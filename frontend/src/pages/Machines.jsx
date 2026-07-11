// frontend/src/pages/Machines.jsx
import { useEffect, useMemo, useState } from "react";
import { Search } from "lucide-react";
import { getMachines } from "../api/api";
import DataTable from "../components/ui/DataTable";
import Badge from "../components/ui/Badge";
import { Input } from "../components/ui/FormField";
import { LoadingState, ErrorState } from "../components/ui/State";
import Card from "../components/ui/Card";

const statusTone = {
  running: "success",
  idle: "neutral",
  maintenance: "warning",
  breakdown: "danger",
  down: "danger",
};

function Machines() {
  const [machines, setMachines] = useState([]);
  const [status, setStatus] = useState("loading");
  const [query, setQuery] = useState("");

  useEffect(() => {
    getMachines()
      .then((data) => {
        setMachines(data);
        setStatus("ready");
      })
      .catch(() => setStatus("error"));
  }, []);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return machines;
    return machines.filter((m) =>
      [m.machine_id, m.machine_name, m.machine_type, m.production_line]
        .filter(Boolean)
        .some((field) => String(field).toLowerCase().includes(q))
    );
  }, [machines, query]);

  const columns = [
    { key: "machine_id", label: "ID", sortable: true },
    {
      key: "machine_name",
      label: "Machine",
      sortable: true,
      render: (row) => <span className="font-medium text-ink">{row.machine_name}</span>,
    },
    { key: "machine_type", label: "Type", sortable: true },
    { key: "production_line", label: "Line", sortable: true },
    {
      key: "power_kw",
      label: "Power",
      sortable: true,
      render: (row) => `${row.power_kw} kW`,
    },
    {
      key: "maintenance_interval_hours",
      label: "Maintenance Interval",
      sortable: true,
      render: (row) => `${row.maintenance_interval_hours} h`,
    },
    {
      key: "status",
      label: "Status",
      sortable: true,
      render: (row) => (
        <Badge tone={statusTone[(row.status || "").toLowerCase()] || "neutral"}>
          {row.status}
        </Badge>
      ),
    },
  ];

  if (status === "loading") return <LoadingState label="Loading machines" />;
  if (status === "error")
    return (
      <ErrorState message="Could not load the machine fleet from the API." />
    );

  return (
    <div className="space-y-4">
      <Card padded={false} className="p-3">
        <div className="flex items-center gap-2 h-9 w-full max-w-sm rounded-lg border border-border bg-surface-alt/70 px-3 transition-colors focus-within:border-accent focus-within:bg-surface">
          <Search size={14} className="text-muted-2 shrink-0" />
          <Input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search by ID, name, type, or line"
            className="h-auto border-0 bg-transparent px-0 focus:border-0 focus:ring-0"
          />
        </div>
      </Card>

      <DataTable
        columns={columns}
        data={filtered}
        emptyMessage="No machines match this search."
      />

      <p className="text-xs text-muted">
        Showing {filtered.length} of {machines.length} machines
      </p>
    </div>
  );
}

export default Machines;