// frontend/src/App.jsx
import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainLayout from "./layouts/MainLayout";
import Dashboard from "./pages/Dashboard";
import Machines from "./pages/Machines";
import Prediction from "./pages/Prediction";
import Alerts from "./pages/Alerts";

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route
                    path="/"
                    element={
                        <MainLayout title="Dashboard" subtitle="Manufacturing overview">
                            <Dashboard />
                        </MainLayout>
                    }
                />
                <Route
                    path="/machines"
                    element={
                        <MainLayout title="Machines" subtitle="Fleet status and specifications">
                            <Machines />
                        </MainLayout>
                    }
                />
                <Route
                    path="/prediction"
                    element={
                        <MainLayout title="AI Prediction" subtitle="Failure risk estimation">
                            <Prediction />
                        </MainLayout>
                    }
                />
                <Route
                    path="/alerts"
                    element={
                        <MainLayout title="Alerts" subtitle="Operational notifications">
                            <Alerts />
                        </MainLayout>
                    }
                />
            </Routes>
        </BrowserRouter>
    );
}

export default App;