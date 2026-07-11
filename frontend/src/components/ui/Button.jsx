// frontend/src/components/ui/Button.jsx
const variants = {
  primary:
    "bg-accent text-white shadow-sm shadow-accent/20 hover:bg-accent-hover hover:shadow-md hover:shadow-accent/25 disabled:bg-accent-border disabled:shadow-none",
  secondary:
    "bg-surface text-ink border border-border hover:bg-surface-alt hover:border-border-strong",
  ghost: "bg-transparent text-muted hover:bg-surface-alt hover:text-ink",
};

const sizes = {
  sm: "h-8 px-3 text-sm",
  md: "h-9 px-4 text-sm",
};

function Button({
  children,
  variant = "primary",
  size = "md",
  className = "",
  type = "button",
  ...props
}) {
  return (
    <button
      type={type}
      className={`inline-flex items-center justify-center gap-2 rounded-lg font-medium transition-all duration-150 active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-60 disabled:active:scale-100 ${variants[variant]} ${sizes[size]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}

export default Button;