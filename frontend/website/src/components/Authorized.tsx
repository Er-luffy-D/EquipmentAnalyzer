import axios from "axios";
import type React from "react";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { apiUrl } from "./constants";

export const Authorized = ({ children }: { children: React.ReactNode }) => {
	const navigate = useNavigate();

	useEffect(() => {
		const checkauth = async () => {
			const access = localStorage.getItem("access_token");
			const refresh = localStorage.getItem("refresh_token");
			if (!access) {
				navigate("/login");
				return;
			}

			try {
				await axios.get(apiUrl + "loggedIn/", {
					headers: {
						Authorization: `Bearer ${access}`,
					},
				});
			} catch (err) {
				console.log(err);
				if (!refresh) {
					navigate("/login");
					return;
				}
				try {
					const refreshRes = await axios.post(apiUrl + "token/refresh/", {
						refresh,
					});

					const newAccess = refreshRes.data.access;

					await axios.get(apiUrl + "loggedIn/", {
						headers: {
							Authorization: `Bearer ${newAccess}`,
						},
					});
				} catch (refreshErr) {
					console.log(refreshErr);
					localStorage.removeItem("access_token");
					localStorage.removeItem("refresh_token");
					navigate("/login");
				}
			}
		};
		checkauth();
	}, [navigate]);

	return <>{children}</>;
};
