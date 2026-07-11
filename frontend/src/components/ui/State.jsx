// frontend/src/components/ui/State.jsx
import { Loader2, AlertTriangle, Inbox } from "lucide-react";

export function LoadingState({ label = "Loading" }) {
  return (
    <div className="flex items-center justify-center gap-2 text-muted text-sm py-16">
      <Loader2 size={16} className="animate-spin" />
      {label}
    </div>
  );
}

export function ErrorState({ message = "Something went wrong" }) {
  return (
    <div className="flex flex-col items-center justify-center gap-2 text-center py-16">
      <AlertTriangle size={20} className="text-danger" />
      <p className="text-sm text-ink font-medium">Unable to load data</p>
      <p className="text-xs text-muted max-w-sm">{message}</p>
    </div>
  );
}

export function EmptyState({ title = "Nothing here yet", message }) {
  return (
    <div className="flex flex-col items-center justify-center gap-2 text-center py-16">
      <Inbox size={20} className="text-muted-2" />
      <p className="text-sm text-ink font-medium">{title}</p>
      {message && (
        <p className="text-xs text-muted max-w-sm">{message}</p>
      )}
    </div>
  );
}