// frontend/src/components/ChartCard.jsx
import Card, { CardHeader } from "./ui/Card";

function ChartCard({ title, subtitle, action, children }) {
  return (
    <Card hover className="transition-shadow">
      <CardHeader title={title} subtitle={subtitle} action={action} />
      <div className="h-64">{children}</div>
    </Card>
  );
}

export default ChartCard;