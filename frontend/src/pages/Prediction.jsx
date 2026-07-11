// frontend/src/pages/Prediction.jsx
import { useState } from "react";
import {
  Bot,
  Play,
  ShieldCheck,
  ShieldAlert,
  ShieldQuestion,
  Loader2,
  Wrench,
  Eye,
  CircleCheck,
} from "lucide-react";
import { predictFailure } from "../api/api";
import Card, { CardHeader } from "../components/ui/Card";
import Button from "../components/ui/Button";
import Badge from "../components/ui/Badge";
import { Field, Input } from "../components/ui/FormField";
import { EmptyState } from "../components/ui/State";

const fields = [
  { key: "runtime_minutes", label: "Runtime (minutes)", placeholder: "600" },
  { key: "utilization_percent", label: "Utilization (%)", placeholder: "75" },
  { key: "health_score", label: "Health score", placeholder: "80" },
  { key: "temperature_c", label: "Temperature (°C)", placeholder: "65" },
  { key: "vibration_mm_s", label: "Vibration (mm/s)", placeholder: "2.1" },
  {
    key: "power_consumption_kw",
    label: "Power consumption (kW)",
    placeholder: "45",
  },
  { key: "avg_energy_kwh", label: "Average energy (kWh)", placeholder: "150" },
  { key: "avg_efficiency", label: "Average efficiency (%)", placeholder: "90" },
  { key: "avg_rejects", label: "Average rejects", placeholder: "5" },
  { key: "avg_downtime", label: "Average downtime (min)", placeholder: "10" },
];

const initialForm = fields.reduce((acc, f) => {
  acc[f.key] = "";
  return acc;
}, {});

function getRiskTier(probability) {
  if (probability >= 70) return "danger";
  if (probability >= 30) return "warning";
  return "success";
}

const tierStyles = {
  danger: {
    ring: "var(--color-danger)",
    soft: "bg-danger-soft text-danger",
    icon: ShieldAlert,
  },
  warning: {
    ring: "var(--color-warning)",
    soft: "bg-warning-soft text-warning",
    icon: ShieldQuestion,
  },
  success: {
    ring: "var(--color-success)",
    soft: "bg-success-soft text-success",
    icon: ShieldCheck,
  },
};

function getRecommendations(probability) {
  if (probability >= 70) {
    return [
      { icon: Wrench, text: "Schedule an immediate inspection for this machine." },
      { icon: Wrench, text: "Reduce load or pause non-critical runs until checked." },
      { icon: Eye, text: "Review recent maintenance and vibration logs for anomalies." },
    ];
  }
  if (probability >= 30) {
    return [
      { icon: Eye, text: "Monitor this machine more closely over the next few shifts." },
      { icon: Wrench, text: "Bring forward the next scheduled maintenance check." },
      { icon: Eye, text: "Watch for rising temperature or vibration trends." },
    ];
  }
  return [
    { icon: CircleCheck, text: "No immediate action required." },
    { icon: CircleCheck, text: "Continue with the standard maintenance schedule." },
    { icon: Eye, text: "Re-run this check if operating conditions change." },
  ];
}

function ProbabilityGauge({ probability, tier }) {
  const radius = 62;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (Math.min(probability, 100) / 100) * circumference;
  const style = tierStyles[tier];

  return (
    <div className="relative w-40 h-40 mx-auto">
      <svg viewBox="0 0 144 144" className="w-full h-full -rotate-90">
        <circle
          cx="72"
          cy="72"
          r={radius}
          fill="none"
          stroke="var(--color-surface-alt)"
          strokeWidth="12"
        />
        <circle
          cx="72"
          cy="72"
          r={radius}
          fill="none"
          stroke={style.ring}
          strokeWidth="12"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          style={{ transition: "stroke-dashoffset 500ms ease-out" }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-3xl font-semibold text-ink tabular-nums tracking-tight">
          {probability}%
        </span>
        <span className="text-xs text-muted mt-0.5">risk score</span>
      </div>
    </div>
  );
}

function Prediction() {
  const [form, setForm] = useState(initialForm);
  const [status, setStatus] = useState("idle");
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  function handleChange(key, value) {
    setForm((prev) => ({ ...prev, [key]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setStatus("loading");
    setError(null);
    try {
      const payload = Object.fromEntries(
        Object.entries(form).map(([k, v]) => [k, Number(v) || 0])
      );
      const data = await predictFailure(payload);
      setResult(data);
      setStatus("ready");
    } catch {
      setError("The prediction service could not be reached. Confirm the API is running.");
      setStatus("error");
    }
  }

  const tier = result ? getRiskTier(result.probability) : "success";
  const tierStyle = tierStyles[tier];
  const TierIcon = tierStyle.icon;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-[1fr_1fr] gap-4 items-start">
      {/* Left: input form */}
      <Card>
        <CardHeader
          title="Machine telemetry input"
          subtitle="Enter current readings to estimate failure risk"
        />
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            {fields.map((f) => (
              <Field key={f.key} label={f.label}>
                <Input
                  type="number"
                  step="any"
                  required
                  placeholder={f.placeholder}
                  value={form[f.key]}
                  onChange={(e) => handleChange(f.key, e.target.value)}
                />
              </Field>
            ))}
          </div>
          <Button type="submit" disabled={status === "loading"} className="w-full">
            {status === "loading" ? (
              <Loader2 size={15} className="animate-spin" />
            ) : (
              <Play size={15} />
            )}
            Run prediction
          </Button>
        </form>
      </Card>

      {/* Right: results and recommendations */}
      <Card className="lg:sticky lg:top-16">
        <CardHeader
          title="Prediction result"
          subtitle="Model output and recommended action"
        />

        {status === "idle" && (
          <EmptyState
            title="No prediction yet"
            message="Fill in the machine telemetry on the left and run a prediction to see results here."
          />
        )}

        {status === "error" && (
          <EmptyState title="Prediction failed" message={error} />
        )}

        {status === "loading" && (
          <div className="flex items-center justify-center gap-2 text-muted text-sm py-16">
            <Loader2 size={16} className="animate-spin" />
            Running model inference
          </div>
        )}

        {status === "ready" && result && (
          <div className="space-y-6">
            <ProbabilityGauge probability={result.probability} tier={tier} />

            <div className="flex items-center justify-center gap-2.5">
              <span className={`w-8 h-8 rounded-lg flex items-center justify-center ${tierStyle.soft}`}>
                <TierIcon size={16} />
              </span>
              <div className="text-center">
                <p className="text-sm font-semibold text-ink">{result.prediction}</p>
                <Badge tone={tier}>{result.probability}% failure probability</Badge>
              </div>
            </div>

            <div>
              <p className="text-xs font-medium text-muted mb-2.5 flex items-center gap-1.5">
                <Bot size={13} /> Recommended actions
              </p>
              <ul className="space-y-2">
                {getRecommendations(result.probability).map((rec, i) => {
                  const RecIcon = rec.icon;
                  return (
                    <li
                      key={i}
                      className="flex items-start gap-2.5 text-sm text-ink bg-surface-alt rounded-lg px-3.5 py-2.5"
                    >
                      <RecIcon size={15} className="text-muted mt-0.5 shrink-0" />
                      <span>{rec.text}</span>
                    </li>
                  );
                })}
              </ul>
            </div>
          </div>
        )}
      </Card>
    </div>
  );
}

export default Prediction;