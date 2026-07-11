// frontend/src/components/Header.jsx
import { Search, Bell, CircleUser } from "lucide-react";

function Header({ title, subtitle }) {
    return (
        <header className="sticky top-0 z-10 h-16 shrink-0 bg-surface/80 backdrop-blur-md border-b border-border px-6 flex items-center justify-between">
            <div className="min-w-0">
                <h1 className="text-[15px] font-semibold text-ink truncate tracking-tight">
                    {title}
                </h1>
                {subtitle && (
                    <p className="text-xs text-muted truncate">{subtitle}</p>
                )}
            </div>

            <div className="flex items-center gap-2">
                <div className="hidden sm:flex items-center gap-2 h-9 w-64 rounded-lg border border-border bg-surface-alt/70 px-3 transition-colors focus-within:border-accent focus-within:bg-surface">
                    <Search size={14} className="text-muted-2 shrink-0" />
                    <input
                        placeholder="Search machines, orders..."
                        className="bg-transparent outline-none text-sm w-full placeholder:text-muted-2"
                    />
                </div>
                <button
                    type="button"
                    className="relative w-9 h-9 rounded-lg flex items-center justify-center text-muted hover:bg-surface-alt hover:text-ink transition-colors"
                    aria-label="Notifications"
                >
                    <Bell size={16} />
                    <span className="absolute top-2 right-2 w-1.5 h-1.5 rounded-full bg-danger" />
                </button>
                <button
                    type="button"
                    className="w-9 h-9 rounded-full flex items-center justify-center text-muted hover:text-ink transition-colors"
                    aria-label="Account"
                >
                    <CircleUser size={22} />
                </button>
            </div>
        </header>
    );
}

export default Header;