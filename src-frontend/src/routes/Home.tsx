import {
  Zap,
  ScrollText,
  Box,
  Brain,
  BarChart3,
  FileText,
  HeartPulse,
  Clock,
  Map,
  Lightbulb,
  ShieldCheck,
  AlertTriangle,
  ArrowUpRight,
} from "lucide-react";

/* ------------------------------------------------------------------ */
/*  Quick-access module shortcuts                                      */
/* ------------------------------------------------------------------ */
const quickAccess = [
  { title: "Grid Overview", icon: Zap, accent: "text-orange-500", bg: "bg-orange-500/10 border-orange-500/20" },
  { title: "Policies", icon: ScrollText, accent: "text-violet-500", bg: "bg-violet-500/10 border-violet-500/20" },
  { title: "Digital Twin", icon: Box, accent: "text-cyan-500", bg: "bg-cyan-500/10 border-cyan-500/20" },
  { title: "Analytics", icon: BarChart3, accent: "text-teal-500", bg: "bg-teal-500/10 border-teal-500/20" },
  { title: "AI Intelligence", icon: Brain, accent: "text-amber-500", bg: "bg-amber-500/10 border-amber-500/20" },
  { title: "Reports", icon: FileText, accent: "text-blue-500", bg: "bg-blue-500/10 border-blue-500/20" },
];

/* ------------------------------------------------------------------ */
/*  Dashboard widget definitions                                       */
/* ------------------------------------------------------------------ */
const widgets: {
  title: string;
  icon: typeof Zap;
  emptyState: string;
  span: string;
}[] = [
  {
    title: "Operational Health",
    icon: HeartPulse,
    emptyState: "No operational data available.",
    span: "sm:col-span-2 lg:col-span-2",
  },
  {
    title: "Recent Events",
    icon: Clock,
    emptyState: "Event log will populate after deployment.",
    span: "sm:col-span-1 lg:col-span-1",
  },
  {
    title: "Grid Map",
    icon: Map,
    emptyState: "Grid visualization will appear here.",
    span: "sm:col-span-2 lg:col-span-2",
  },
  {
    title: "AI Recommendations",
    icon: Lightbulb,
    emptyState: "AI recommendations will be available after deployment.",
    span: "sm:col-span-1 lg:col-span-1",
  },
  {
    title: "Active Policies",
    icon: ShieldCheck,
    emptyState: "No active policies configured.",
    span: "sm:col-span-1 lg:col-span-1",
  },
  {
    title: "Alerts",
    icon: AlertTriangle,
    emptyState: "No active alerts at this time.",
    span: "sm:col-span-1 lg:col-span-1",
  },
];

/* ------------------------------------------------------------------ */
/*  Component                                                          */
/* ------------------------------------------------------------------ */
export default function Home() {
  return (
    <div className="space-y-8 py-2">
      {/* ── Welcome ────────────────────────────────────────────────── */}
      <section className="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4">
        <div>
          <p className="text-xs font-mono text-slate-400 dark:text-slate-500 tracking-widest uppercase mb-1">
            Welcome back
          </p>
          <h1 className="text-xl sm:text-2xl font-heading font-bold tracking-tight text-slate-900 dark:text-[#F8FAFC]">
            Grid Policy Orchestrator
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-1 max-w-md leading-relaxed">
            Manage smart grid operations, monitor infrastructure, and prepare AI&#8209;powered
            decision making.
          </p>
        </div>
        <div className="flex-shrink-0">
          <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-[3px] border border-blue-500/20 bg-blue-500/10 text-blue-500 text-[11px] font-mono">
            <span className="w-1.5 h-1.5 rounded-full bg-blue-500 animate-pulse" />
            Authentication required to unlock live data
          </span>
        </div>
      </section>

      {/* ── Quick Access ───────────────────────────────────────────── */}
      <section>
        <h2 className="text-[10px] font-mono font-bold text-slate-400 dark:text-slate-500 uppercase tracking-widest mb-3">
          Quick Access
        </h2>
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
          {quickAccess.map((m) => (
            <div
              key={m.title}
              className="group border border-slate-200 dark:border-[#1E293B] bg-white dark:bg-[#151A21]/50 rounded-[3px] p-4 flex flex-col items-start gap-3 hover:border-slate-300 dark:hover:border-[#2A313C] transition-colors cursor-not-allowed"
            >
              <div className={`w-8 h-8 rounded-[3px] border flex items-center justify-center ${m.bg}`}>
                <m.icon className={`w-4 h-4 ${m.accent}`} />
              </div>
              <div className="flex items-center gap-1 w-full">
                <span className="text-xs font-medium text-slate-700 dark:text-slate-300 truncate">
                  {m.title}
                </span>
                <ArrowUpRight className="w-3 h-3 text-slate-400 dark:text-slate-600 opacity-0 group-hover:opacity-100 transition-opacity flex-shrink-0" />
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* ── Dashboard Widgets ──────────────────────────────────────── */}
      <section>
        <h2 className="text-[10px] font-mono font-bold text-slate-400 dark:text-slate-500 uppercase tracking-widest mb-3">
          Dashboard
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {widgets.map((w) => (
            <div
              key={w.title}
              className={`border border-slate-200 dark:border-[#1E293B] bg-white dark:bg-[#151A21]/40 rounded-[3px] p-5 flex flex-col ${w.span}`}
            >
              {/* Widget Header */}
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-2">
                  <w.icon className="w-4 h-4 text-slate-400 dark:text-slate-500" />
                  <h3 className="text-xs font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wide">
                    {w.title}
                  </h3>
                </div>
                <span className="text-[9px] font-mono text-slate-400 dark:text-slate-600 uppercase">
                  Pending
                </span>
              </div>

              {/* Empty State */}
              <div className="flex-1 flex items-center justify-center min-h-[100px]">
                <div className="text-center px-4">
                  <div className="w-10 h-10 mx-auto rounded-full bg-slate-100 dark:bg-[#1C222B] border border-slate-200 dark:border-[#2A313C] flex items-center justify-center mb-3">
                    <w.icon className="w-5 h-5 text-slate-300 dark:text-slate-600" />
                  </div>
                  <p className="text-xs text-slate-400 dark:text-slate-500 leading-relaxed max-w-[200px] mx-auto">
                    {w.emptyState}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
