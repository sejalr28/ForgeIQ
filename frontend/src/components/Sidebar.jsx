// frontend/src/components/Sidebar.jsx
import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  Cpu,
  Bot,
  TriangleAlert,
  ChevronsLeft,
  ChevronsRight,
} from "lucide-react";

const menu = [
  { to: "/", icon: LayoutDashboard, label: "Dashboard", end: true },
  { to: "/machines", icon: Cpu, label: "Machines" },
  { to: "/prediction", icon: Bot, label: "AI Prediction" },
  { to: "/alerts", icon: TriangleAlert, label: "Alerts" },
];

function Sidebar({ collapsed, onToggle }) {
  return (
    <aside
      className={`h-screen shrink-0 bg-surface border-r border-border flex flex-col transition-[width] duration-300 ease-[cubic-bezier(0.4,0,0.2,1)] ${
        collapsed ? "w-[72px]" : "w-64"
      }`}
    >
      <div className="flex items-center gap-3 px-4 h-16 border-b border-border">
        <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-accent to-accent-hover flex items-center justify-center shrink-0 shadow-sm shadow-accent/30">
          <span className="text-white text-sm font-bold tracking-tight">F</span>
        </div>
        {!collapsed && (
          <div className="min-w-0">
            <p className="text-sm font-semibold text-ink leading-tight truncate tracking-tight">
              ForgeIQ
            </p>
            <p className="text-[11px] text-muted leading-tight truncate">
              Manufacturing AI
            </p>
          </div>
        )}
      </div>

      <nav className="flex-1 px-3 py-5 space-y-1">
        {menu.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              title={collapsed ? item.label : undefined}
              className={({ isActive }) =>
                `group relative flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all duration-150 ${
                  isActive
                    ? "bg-accent-soft text-accent"
                    : "text-muted hover:bg-surface-alt hover:text-ink"
                } ${collapsed ? "justify-center" : ""}`
              }
            >
              {({ isActive }) => (
                <>
                  <span
                    className={`absolute left-0 top-1/2 -translate-y-1/2 w-[3px] rounded-full bg-accent transition-all duration-200 ${
                      isActive ? "h-5 opacity-100" : "h-0 opacity-0"
                    }`}
                  />
                  <Icon
                    size={18}
                    strokeWidth={2}
                    className="shrink-0 transition-transform duration-150 group-hover:scale-105"
                  />
                  {!collapsed && <span className="truncate">{item.label}</span>}
                </>
              )}
            </NavLink>
          );
        })}
      </nav>

      <div className="p-3 border-t border-border">
        <button
          type="button"
          onClick={onToggle}
          className={`flex items-center gap-3 w-full rounded-lg px-3 py-2.5 text-sm font-medium text-muted hover:bg-surface-alt hover:text-ink transition-colors duration-150 ${
            collapsed ? "justify-center" : ""
          }`}
        >
          {collapsed ? (
            <ChevronsRight size={18} />
          ) : (
            <>
              <ChevronsLeft size={18} />
              <span>Collapse</span>
            </>
          )}
        </button>
      </div>
    </aside>
  );
}

export default Sidebar;