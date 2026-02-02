import { LogOut, Upload, FileText, RefreshCw } from "lucide-react";
import { useCallback, useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { toast, ToastContainer } from "react-toastify";
import { apiUrl } from "./constants";

type Dataset = {
	id: number;
	total_count: number;
	avg_flowrate: number;
	avg_temperature: number;
};

export const Dashboard = () => {
	const navigate = useNavigate();
	
	const [data, setData] = useState<Dataset[]>([]);
	const [selectedId, setSelectedId] = useState<number | null>(null);

	const headers = useMemo(() => {
		const token = localStorage.getItem("access_token");
		return {
			Authorization: `Bearer ${token}`,
		};
	}, []);

	const logout = () => {
		localStorage.removeItem("access_token");
		localStorage.removeItem("refresh_token");
		navigate("/login");
	};

	const updateData = (data: Dataset[]) => {
		setData(data);
	};
	const fetchSummary = useCallback(async () => {
		try {
			const res = await axios.get(apiUrl+"summary/", { headers });
			updateData(res.data);
		} catch {
			toast.error("Failed to fetch summary");
		}
	}, [headers]);

	const uploadCSV = useCallback(
		async (file: File) => {
			const formData = new FormData();
			formData.append("file", file);

			try {
				await axios.post(apiUrl+"upload/", formData, { headers });
				toast.success("CSV uploaded successfully");
				fetchSummary();
			} catch {
				toast.error("CSV upload failed");
			}
		},
		[headers, fetchSummary],
	);

	const downloadPDF = useCallback(async () => {
		if (!selectedId) {
			toast.error("Please select a dataset first");
			return;
		}

		try {
			const res = await axios.get(`${apiUrl}report/${selectedId}/`, {
				headers,
				responseType: "blob",
			});

			const blob = new Blob([res.data], { type: "application/pdf" });
			const url = window.URL.createObjectURL(blob);

			const link = document.createElement("a");
			link.href = url;
			link.download = `report_${selectedId}.pdf`;
			document.body.appendChild(link);
			link.click();
			link.remove();
		} catch {
			toast.error("Failed to download PDF");
		}
	}, [headers, selectedId]);

	useEffect(() => {
		fetchSummary();
	}, [fetchSummary]);

	const latest = data[data.length - 1];

	return (
		<div className="min-h-screen bg-gray-100">
			<header className="bg-white shadow-sm px-8 py-4 flex justify-between items-center">
				<h1 className="text-xl font-bold text-gray-800">Chemical Equipment Dashboard</h1>

				<button onClick={logout} className="flex items-center gap-2 text-red-600 hover:text-red-700">
					<LogOut size={16} />
					Logout
				</button>
			</header>

			<main className="p-8 space-y-8">
				<div className="flex flex-wrap gap-4">
					<label className="cursor-pointer flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg">
						<Upload size={16} />
						Upload CSV
						<input type="file" hidden accept=".csv" onChange={(e) => e.target.files && uploadCSV(e.target.files[0])} />
					</label>

					<button
						onClick={fetchSummary}
						className="flex items-center gap-2 bg-gray-800 hover:bg-gray-900 text-white px-4 py-2 rounded-lg"
					>
						<RefreshCw size={16} />
						Refresh Summary
					</button>

					<button
						onClick={downloadPDF}
						className="flex items-center gap-2 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg"
					>
						<FileText size={16} />
						Download PDF
					</button>
				</div>

				<div className="grid grid-cols-1 md:grid-cols-3 gap-6">
					<StatCard title="Total Records" value={latest?.total_count ?? "—"} />
					<StatCard
						title="Avg Flowrate"
						value={latest?.avg_flowrate !== undefined ? latest.avg_flowrate.toFixed(2) : "—"}
					/>
					<StatCard
						title="Avg Temperature"
						value={latest?.avg_temperature !== undefined ? latest.avg_temperature.toFixed(2) : "—"}
					/>
				</div>

				<div className="bg-white rounded-xl shadow p-6">
					<h2 className="text-lg font-semibold mb-4">Dataset Summary</h2>

					{data.length === 0 ? (
						<p className="text-gray-500 text-center">No datasets available</p>
					) : (
						<table className="w-full border text-left">
							<thead className="bg-gray-100">
								<tr>
									<th className="p-2">ID</th>
									<th className="p-2">Total</th>
									<th className="p-2">Avg Flowrate</th>
									<th className="p-2">Avg Temperature</th>
									<th className="p-2">chart</th>
								</tr>
							</thead>
							<tbody>
								{data.map((d) => (
									<tr
										key={d.id}
										onClick={() => setSelectedId(d.id)}
										className={`cursor-pointer hover:bg-blue-50 ${selectedId === d.id ? "bg-blue-100" : ""}`}
									>
										<td className="p-2">{d.id}</td>
										<td className="p-2">{d.total_count}</td>
										<td className="p-2">{d.avg_flowrate.toFixed(2)}</td>
										<td className="p-2">{d.avg_temperature.toFixed(2)}</td>
										<td className="p-2">
											<a href={`https://equipment-analyzer.vercel.app/dashboard/report/${d.id}`}> Click here</a>
										</td>
									</tr>
								))}
							</tbody>
						</table>
					)}
				</div>
			</main>
			<ToastContainer />
		</div>
	);
};

const StatCard = ({ title, value }: { title: string; value: string | number }) => (
	<div className="bg-white rounded-xl shadow p-6">
		<p className="text-sm text-gray-500">{title}</p>
		<p className="text-2xl font-bold mt-2">{value}</p>
	</div>
);
