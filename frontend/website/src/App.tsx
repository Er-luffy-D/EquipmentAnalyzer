import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Home } from "./components/Home";
import { Signup } from "./components/Signup";
import { Login } from "./components/Login";
import { Dashboard } from "./components/Dashboard";
import { Error } from "./components/Error";
import { Authorized } from "./components/Authorized";

const App = () => {
	return (
		<>
			<BrowserRouter>
				<Routes>
					<Route path="/" element={<Home />}></Route>
					<Route path="/signup" element={<Signup />}></Route>
					<Route path="/login" element={<Login />}></Route>
					<Route
						path="/dashboard"
						element={
							<Authorized>
								<Dashboard />
							</Authorized>
						}
					></Route>
					<Route path="*" element={<Error />}></Route>
				</Routes>
			</BrowserRouter>
		</>
	);
};

export default App;
