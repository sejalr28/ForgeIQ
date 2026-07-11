// frontend/src/components/ui/DataTable.jsx
import { useMemo, useState } from "react";
import { ChevronUp, ChevronDown, ChevronsUpDown } from "lucide-react";

function DataTable({ columns, data, emptyMessage = "No records to display" }) {
    const [sortKey, setSortKey] = useState(null);
    const [sortDir, setSortDir] = useState("asc");

    const sorted = useMemo(() => {
        if (!sortKey) return data;
        const copy = [...data];
        copy.sort((a, b) => {
            const av = a[sortKey];
            const bv = b[sortKey];
            if (av === bv) return 0;
            const result = av > bv ? 1 : -1;
            return sortDir === "asc" ? result : -result;
        });
        return copy;
    }, [data, sortKey, sortDir]);

    function toggleSort(key) {
        if (sortKey !== key) {
            setSortKey(key);
            setSortDir("asc");
        } else {
            setSortDir((d) => (d === "asc" ? "desc" : "asc"));
        }
    }

    return (
        <div className="overflow-x-auto rounded-xl border border-border bg-surface">
            <table className="w-full text-sm border-collapse">
                <thead>
                    <tr className="bg-surface-alt/60 border-b border-border">
                        {columns.map((col) => (
                            <th
                                key={col.key}
                                className="text-left font-medium text-muted px-4 py-3 select-none whitespace-nowrap"
                            >
                                {col.sortable ? (
                                    <button
                                        type="button"
                                        onClick={() => toggleSort(col.key)}
                                        className="inline-flex items-center gap-1 hover:text-ink transition-colors"
                                    >
                                        {col.label}
                                        {sortKey === col.key ? (
                                            sortDir === "asc" ? (
                                                <ChevronUp size={13} />
                                            ) : (
                                                <ChevronDown size={13} />
                                            )
                                        ) : (
                                            <ChevronsUpDown size={13} className="text-muted-2" />
                                        )}
                                    </button>
                                ) : (
                                    col.label
                                )}
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {sorted.length === 0 ? (
                        <tr>
                            <td
                                colSpan={columns.length}
                                className="px-4 py-10 text-center text-muted"
                            >
                                {emptyMessage}
                            </td>
                        </tr>
                    ) : (
                        sorted.map((row, i) => (
                            <tr
                                key={row.id ?? i}
                                className="border-b border-border last:border-0 transition-colors duration-100 hover:bg-accent-soft/40"
                            >
                                {columns.map((col) => (
                                    <td
                                        key={col.key}
                                        className="px-4 py-3 text-ink whitespace-nowrap"
                                    >
                                        {col.render ? col.render(row) : row[col.key]}
                                    </td>
                                ))}
                            </tr>
                        ))
                    )}
                </tbody>
            </table>
        </div>
    );
}

export default DataTable;