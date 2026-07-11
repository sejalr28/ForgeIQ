// frontend/src/pages/Alerts.jsx
import { useEffect, useState } from "react";
import {
    TriangleAlert,
    ListFilter,
    Clock3,
    Cpu,
    BadgeCheck,
    Layers,
} from "lucide-react";
import { getDashboardOverview } from "../api/api";
import Card, { CardHeader } from "../components/ui/Card";
import KPICard from "../components/KPICard";
import { LoadingState, ErrorState } from "../components/ui/State";

const plannedCapabilities = [
    { icon: TriangleAlert, label: "Severity level" },
    { icon: Cpu, label: "Affected machine" },
    { icon: Clock3, label: "Timestamp" },
    { icon: BadgeCheck, label: "Acknowledgment status" },
];

function Alerts() {
    const [overview, setOverview] = useState(null);
    const [status, setStatus] = useState("loading");

    useEffect(() => {
        getDashboardOverview()
            .then((data) => {
                setOverview(data);
                setStatus("ready");
            })
            .catch(() => setStatus("error"));
    }, []);

    if (status === "loading") return <LoadingState label="Loading alerts" />;
    if (status === "error")
        return <ErrorState message="Could not load alert data from the API." />;

    return (
        <div className="space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <KPICard
                    icon={TriangleAlert}
                    label="Total Alerts Logged"
                    value={overview.alerts}
                    tone="warning"
                    hint="All-time total"
                />
            </div>

            <Card>
                <CardHeader
                    title="Recent alerts"
                    subtitle="Individual alert records, most recent first"
                    action={
                        <span className="flex items-center gap-1.5 text-xs text-muted-2">
                            <ListFilter size={13} />
                            Filtering unavailable
                        </span>
                    }
                />

                <div className="flex flex-col items-center text-center py-12 px-6">
                    <span className="w-12 h-12 rounded-xl bg-warning-soft text-warning flex items-center justify-center mb-4">
                        <Layers size={22} />
                    </span>
                    <p className="text-sm font-semibold text-ink">
                        Alert feed not available yet
                    </p>
                    <p className="text-xs text-muted max-w-sm mt-1.5 leading-relaxed">
                        The API currently returns only a total alert count, not individual
                        alert records. Listing, filtering, and acknowledging alerts here
                        requires a dedicated alerts endpoint on the backend.
                    </p>

                    <div className="grid grid-cols-2 gap-2.5 mt-6 w-full max-w-sm">
                        {plannedCapabilities.map((item) => {
                            const Icon = item.icon;
                            return (
                                <div
                                    key={item.label}
                                    className="flex items-center gap-2 rounded-lg border border-border bg-surface-alt/60 px-3 py-2 text-xs text-muted"
                                >
                                    <Icon size={13} className="text-muted-2 shrink-0" />
                                    {item.label}
                                </div>
                            );
                        })}
                    </div>
                </div>
            </Card>
        </div>
    );
}

export default Alerts;