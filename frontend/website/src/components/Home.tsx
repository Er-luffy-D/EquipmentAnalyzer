import { useState } from "react";
import { Link } from "react-router-dom";

export const Home = () => {
	const [loggedIn] = useState<boolean>(() => {
		return localStorage.getItem("access_token") !== null;
	});

	return (
		<div className="bg-[url('/back.png')] bg-cover  min-h-screen text-white p-8">
			<header className="flex justify-end max-w-7xl mx-auto">
				{!loggedIn ? (
					<Link to={"/login"}>
						<button className="px-6 py-2 border border-gray-700 rounded-lg hover:bg-gray-900 transition-colors duration-300 text-gray-300 hover:text-white">
							Login
						</button>
					</Link>
				) : (
					<Link to={"/dashboard"}>
						<button className="px-6 py-2 border border-gray-700 rounded-lg hover:bg-gray-900 transition-colors duration-300 text-gray-300 hover:text-white">
							Dashboard
						</button>
					</Link>
				)}
			</header>

			<main className="flex flex-col items-center justify-center min-h-[80vh] ">
				<div className="bg-gray-600/30 p-5 rounded-2xl flex flex-col items-center justify-center gap-4 backdrop-blur-2xl">
					<h1 className="text-5xl md:text-7xl font-bold text-center mb-8 tracking-tight">
						<span className="text-white  text-shadow-lg text-shadow-black">Chemical Equipment</span>
						<br />
						<span className="text-white text-shadow-lg text-shadow-black">Analyzer</span>
					</h1>

					<p className="text-white text-lg mb-12 max-w-2xl text-center ">
						Upload CSV file and see the magic. Precision, safety, and efficiency for industrial applications.
					</p>

					<a
						href="https://github.com/Er-luffy-D/EquipmentAnalyzer"
						target="_blank"
						rel="noopener noreferrer"
						className="group relative inline-flex items-center gap-3 px-8 py-4 bg-linear-to-r from-gray-900 to-gray-800 rounded-xl hover:from-gray-800 hover:to-gray-700 transition-all duration-300 border border-gray-800 hover:border-gray-700 shadow-lg hover:shadow-xl hover:scale-[1.02]"
					>
						<div className="absolute inset-0 bg-linear-to-r from-cyan-500/10 to-emerald-500/10 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
						<svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
							<path
								fillRule="evenodd"
								d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"
								clipRule="evenodd"
							/>
						</svg>
						<span className="text-lg font-medium relative">View on GitHub</span>
					</a>
				</div>
			</main>

			<footer className="absolute bottom-8 left-0 right-0 text-center">
				<p className="text-gray-600 text-sm relative">
					<span className="relative top-2">Made by Piyush Dixit</span>
					<img className="h-14 inline" src="cute.gif"></img>
				</p>
			</footer>
		</div>
	);
};
