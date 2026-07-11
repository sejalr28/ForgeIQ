// frontend/src/layouts/MainLayout.jsx
import { useState } from "react";
import { useLocation } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import Header from "../components/Header";

function MainLayout({ title, subtitle, children }) {
  const [collapsed, setCollapsed] = useState(false);
  const location = useLocation();

  return (
    <div className="flex h-screen bg-bg overflow-hidden">
      <Sidebar collapsed={collapsed} onToggle={() => setCollapsed((c) => !c)} />
      <div className="flex-1 flex flex-col min-w-0">
        <Header title={title} subtitle={subtitle} />
        <main className="flex-1 overflow-auto px-6 py-6">
          <div key={location.pathname} className="page-transition">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}

export default MainLayout;