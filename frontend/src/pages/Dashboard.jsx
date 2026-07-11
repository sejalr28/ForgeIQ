// frontend/src/pages/Dashboard.jsx
import { useEffect, useMemo, useState } from "react";
import {
  Factory,
  Clock,
  RefreshCw,
  Cpu,
  Users,
  ClipboardList,
  TriangleAlert,
  Zap,
  Building2,
} from "lucide-react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { getDashboardOverview, getFactories, getMachines } from "../api/api";
import KPICard from "../components/KPICard";
import ChartCard from "../components/ChartCard";
import Card from "../components/ui/Card";
import { LoadingState, ErrorState } from "../components/ui/State";

function getActiveShift(date = new Date()) {
  const hour = date.getHours();
  if (hour >= 6 && hour < 14) return "Shift A · 06:00–14:00";
  if (hour >= 14 && hour < 22) return "Shift B · 14:00–22:00";
  return "Shift C · 22:00–06:00";
}

function groupCount(list, key) {
  const counts = {};
  for (const item of list) {
    const value = item[key] || "Unspecified";
    counts[value] = (counts[value] || 0) + 1;
  }
  return Object.entries(counts).map(([name, count]) => ({ name, count }));
}

function SummaryItem({ icon: Icon, label, value }) {
  return (
    <div className="flex items-center gap-3 px-5 py-3.5 first:pl-0 last:pr-0">
      <span className="w-9 h-9 rounded-lg bg-accent-soft text-accent flex items-center justify-center shrink-0">
        <Icon size={15} strokeWidth={2} />
      </span>
      <div className="min-w-0">
        <p className="text-xs text-muted leading-tight">{label}</p>
        <p className="text-sm font-medium text-ink leading-tight truncate">
          {value}
        </p>
      </div>
    </div>
  );
}

function ChartTooltip({ active, payload, label }) {
  if (!active || !payload || !payload.length) return null;
  return (
    <div className="rounded-lg border border-border bg-surface px-3 py-2 shadow-lg shadow-ink/5 text-xs">
      <p className="font-medium text-ink mb-0.5">{label}</p>
      <p className="text-muted">
        Machines: <span className="font-semibold text-ink">{payload[0].value}</span>
      </p>
    </div>
  );
}

function Dashboard() {
  const [overview, setOverview] = useState(null);
  const [factories, setFactories] = useState([]);
  const [machines, setMachines] = useState([]);
  const [lastSync, setLastSync] = useState(null);
  const [status, setStatus] = useState("loading");

  async function load() {
    setStatus("loading");
    try {
      const [overviewData, factoriesData, machinesData] = await Promise.all([
        getDashboardOverview(),
        getFactories(),
        getMachines(),
      ]);
      setOverview(overviewData);
      setFactories(factoriesData);
      setMachines(machinesData);
      setLastSync(new Date());
      setStatus("ready");
    } catch {
      setStatus("error");
    }
  }

  useEffect(() => {
    load();
  }, []);

  const machinesOnline = useMemo(
    () => machines.filter((m) => (m.status || "").toLowerCase() === "running").length,
    [machines]
  );

  const byLine = useMemo(() => groupCount(machines, "production_line"), [machines]);
  const byType = useMemo(() => groupCount(machines, "machine_type"), [machines]);

  const factoryLabel =
    factories.length === 0
      ? "—"
      : factories.length === 1
      ? factories[0].factory_name
      : `${factories.length} Factories`;

  if (status === "loading") return <LoadingState label="Loading dashboard" />;
  if (status === "error")
    return (
      <ErrorState message="Could not reach the ForgeIQ API. Confirm the backend is running and reachable from the browser." />
    );

  return (
    <div className="space-y-6">
      {/* Operational summary strip */}
      <Card padded={false} className="px-5 py-1">
        <div className="flex flex-wrap divide-x divide-border">
          <SummaryItem icon={Factory} label="Factory" value={factoryLabel} />
          <SummaryItem icon={Clock} label="Active Shift" value={getActiveShift()} />
          <SummaryItem
            icon={RefreshCw}
            label="Last Data Sync"
            value={lastSync ? lastSync.toLocaleTimeString() : "—"}
          />
          <SummaryItem
            icon={Cpu}
            label="Machines Online"
            value={`${machinesOnline} / ${machines.length}`}
          />
        </div>
      </Card>

      {/* KPI grid */}
      <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-4">
        <KPICard
          icon={Building2}
          label="Factories"
          value={overview.factories}
          hint="Active sites"
        />
        <KPICard
          icon={Users}
          label="Employees"
          value={overview.employees}
          hint="Across factories"
        />
        <KPICard
          icon={Cpu}
          label="Machines"
          value={overview.machines}
          hint={`${machinesOnline} online`}
        />
        <KPICard
          icon={ClipboardList}
          label="Production Orders"
          value={overview.production_orders}
          hint="All-time total"
        />
        <KPICard
          icon={TriangleAlert}
          label="Alerts"
          value={overview.alerts}
          tone="warning"
          hint="All-time total"
        />
        <KPICard
          icon={Zap}
          label="Energy Used"
          value={overview.total_energy_kwh.toLocaleString()}
          suffix="kWh"
          hint="Dataset period"
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <ChartCard
          title="Machines by production line"
          subtitle="Installed base per line"
        >
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={byLine} margin={{ left: -20, right: 8 }}>
              <defs>
                <linearGradient id="barGradientVertical" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="var(--color-accent)" stopOpacity={1} />
                  <stop offset="100%" stopColor="var(--color-accent)" stopOpacity={0.55} />
                </linearGradient>
              </defs>
              <CartesianGrid stroke="var(--color-border)" vertical={false} strokeDasharray="3 3" />
              <XAxis
                dataKey="name"
                tick={{ fontSize: 12, fill: "var(--color-muted)" }}
                axisLine={{ stroke: "var(--color-border)" }}
                tickLine={false}
              />
              <YAxis
                allowDecimals={false}
                tick={{ fontSize: 12, fill: "var(--color-muted)" }}
                axisLine={false}
                tickLine={false}
              />
              <Tooltip cursor={{ fill: "var(--color-surface-alt)" }} content={<ChartTooltip />} />
              <Bar
                dataKey="count"
                fill="url(#barGradientVertical)"
                radius={[6, 6, 0, 0]}
                maxBarSize={48}
              />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Machines by type" subtitle="Fleet composition">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={byType} layout="vertical" margin={{ left: 8, right: 16 }}>
              <defs>
                <linearGradient id="barGradientHorizontal" x1="0" y1="0" x2="1" y2="0">
                  <stop offset="0%" stopColor="var(--color-accent)" stopOpacity={0.55} />
                  <stop offset="100%" stopColor="var(--color-accent)" stopOpacity={1} />
                </linearGradient>
              </defs>
              <CartesianGrid stroke="var(--color-border)" horizontal={false} strokeDasharray="3 3" />
              <XAxis
                type="number"
                allowDecimals={false}
                tick={{ fontSize: 12, fill: "var(--color-muted)" }}
                axisLine={false}
                tickLine={false}
              />
              <YAxis
                type="category"
                dataKey="name"
                width={120}
                tick={{ fontSize: 12, fill: "var(--color-muted)" }}
                axisLine={false}
                tickLine={false}
              />
              <Tooltip cursor={{ fill: "var(--color-surface-alt)" }} content={<ChartTooltip />} />
              <Bar
                dataKey="count"
                fill="url(#barGradientHorizontal)"
                radius={[0, 6, 6, 0]}
                maxBarSize={28}
              />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>
    </div>
  );
}

export default Dashboard;