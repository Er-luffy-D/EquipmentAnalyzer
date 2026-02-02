import axios from "axios";
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { toast, ToastContainer } from "react-toastify";
import { apiUrl } from "./constants";

export const Signup = () => {
	const [username, setUserName] = useState<string>("");
	const [password, setPassword] = useState<string>("");
	const navigate = useNavigate();
	const registerApi = async () => {
		if (!username || !password) {
			toast.error("Username and password are required");
			return;
		}

		if (password.length < 6) {
			toast.error("Password must be at least 6 characters");
			return;
		}

		try {
			const apiurl = apiUrl+"signup/";
			const response = await axios.post(apiurl, {
				username,
				password,
			});

			if (response.status === 201) {
				toast.success("Account created successfully");

				setTimeout(() => {
					navigate("/login");
				}, 1000);
			}
		} catch (err: any) {
			const status = err.response?.status;

			if (status === 400) {
				toast.error("User already exists");
			} else {
				toast.error("Something went wrong. Try again.");
				console.error(err);
			}
		}
	};

	return (
		<div className="bg-[url('/back.png')] bg-cover  min-h-screen text-black p-8">
			<main className="flex flex-col items-center justify-center min-h-[80vh] ">
				<div className="bg-gray-600/30 p-5 w-1/2 rounded-2xl flex flex-col items-center justify-center gap-4 backdrop-blur-2xl">
					<div className="max-w-xl mx-auto m-10 w-full p-14 bg-white rounded-lg shadow-md">
						<h2 className="text-2xl font-bold text-center text-gray-800 mb-6">Register</h2>
						<div className="space-y-4">
							<div>
								<label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-1">
									Username
								</label>
								<input
									type="text"
									id="username"
									onChange={(e) => setUserName(e.target.value)}
									value={username}
									className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
									placeholder="Enter your username"
								/>
							</div>

							<div>
								<label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
									Password
								</label>
								<input
									type="password"
									id="password"
									onChange={(e) => setPassword(e.target.value)}
									value={password}
									className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
									placeholder="Enter your password"
								/>
							</div>

							<button
								onClick={registerApi}
								className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md transition duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
							>
								Register
							</button>

							<div className="text-center pt-4 border-t border-gray-200">
								<Link
									to="/login"
									className="text-blue-600 hover:text-blue-800 font-medium transition inline-flex items-center"
								>
									<span>Already a User?</span>
									<span className="ml-1 underline">Login here</span>
								</Link>
							</div>
						</div>
					</div>
				</div>
			</main>
			<ToastContainer />
		</div>
	);
};
