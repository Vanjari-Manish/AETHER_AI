import { Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { useAuthorization } from "../hooks/useAuthorization";
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
  Lock,
  Activity,
  CheckCircle2,
} from "lucide-react";

/* ------------------------------------------------------------------ */
/*  Quick-access module shortcuts                                      */
/* ------------------------------------------------------------------ */
const quickAccessItems = [
  { title: "Grid Overview", icon: Zap, accent: "text-orange-500", bg: "bg-orange-500/10 border-orange-500/20", path: "/grid-overview", permission: "grid:view" },
  { title: "Policies", icon: ScrollText, accent: "text-violet-500", bg: "bg-violet-500/10 border-violet-500/20", path: "/policy-engine", permission: "policies:view" },
  { title: "Digital Twin", icon: Box, accent: "text-cyan-500", bg: "bg-cyan-500/10 border-cyan-500/20", path: "/grid-overview", permission: "grid:view" },
  { title: "Analytics", icon: BarChart3, accent: "text-teal-500", bg: "bg-teal-500/10 border-teal-500/20", path: "/analytics", permission: "analytics:view" },
  { title: "AI Intelligence", icon: Brain, accent: "text-amber-500", bg: "bg-amber-500/10 border-amber-500/20", path: "/admin", permission: "admin:view" },
  { title: "Reports", icon: FileText, accent: "text-blue-500", bg: "bg-blue-500/10 border-blue-500/20", path: "/reports", permission: "reports:view" },
];

export default function Home() {
  const { profile } = useAuth();
  const { checkPermission } = useAuthorization();

  return (
    <div className="space-y-8 py-2 select-text">
      {/* ── Welcome Header ────────────────────────────────────────── */}
      <section className="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4 border-b border-slate-200 dark:border-[#1E293B] pb-6">
        <div>
          <p className="text-[10px] font-mono text-slate-400 dark:text-slate-500 tracking-widest uppercase mb-1.5">
            Operational Clearance // {profile?.role || "Guest"}
          </p>
          <h1 className="text-xl sm:text-2xl font-heading font-bold tracking-tight text-slate-900 dark:text-[#F8FAFC]">
            Grid Policy Orchestrator
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-1 max-w-xl leading-relaxed">
            Welcome back, <span className="font-semibold text-slate-800 dark:text-slate-200">{profile?.full_name || "Grid Operator"}</span>. 
            Manage smart grid configurations and monitor localized autonomous agents under {profile?.organization || "GPO Corp"} boundaries.
          </p>
        </div>
        <div className="flex-shrink-0">
          <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-[3px] border border-emerald-500/20 bg-emerald-500/10 text-emerald-500 text-[11px] font-mono font-semibold">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
            SYS.STATUS // NOMINAL
          </span>
        </div>
      </section>

      {/* ── Quick Access ───────────────────────────────────────────── */}
      <section>
        <h2 className="text-[10px] font-mono font-bold text-slate-400 dark:text-slate-500 uppercase tracking-widest mb-3">
          Console Modules
        </h2>
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
          {quickAccessItems.map((m) => {
            const isAllowed = checkPermission(m.permission);

            if (isAllowed) {
              return (
                <Link
                  key={m.title}
                  to={m.path}
                  className="group border border-slate-200 dark:border-[#1E293B] bg-white dark:bg-[#151A21]/50 rounded-[3px] p-4 flex flex-col items-start gap-3 hover:border-[#FF7A1A]/80 dark:hover:border-[#FF7A1A]/60 transition-all hover:bg-slate-50 dark:hover:bg-[#151A21] shadow-sm focus-visible:ring-1 focus-visible:ring-[#FF7A1A]"
                >
                  <div className={`w-8 h-8 rounded-[3px] border flex items-center justify-center ${m.bg}`}>
                    <m.icon className={`w-4 h-4 ${m.accent}`} />
                  </div>
                  <div className="flex items-center justify-between w-full">
                    <span className="text-xs font-semibold text-slate-700 dark:text-slate-300 truncate">
                      {m.title}
                    </span>
                    <ArrowUpRight className="w-3.5 h-3.5 text-slate-400 dark:text-slate-600 opacity-0 group-hover:opacity-100 transition-opacity flex-shrink-0" />
                  </div>
                </Link>
              );
            }

            return (
              <div
                key={m.title}
                className="border border-slate-200/50 dark:border-[#1E293B]/40 bg-slate-50/50 dark:bg-[#0F1318]/50 rounded-[3px] p-4 flex flex-col items-start gap-3 opacity-50 cursor-not-allowed"
                title="Clearance required to access this module"
              >
                <div className="w-8 h-8 rounded-[3px] border border-slate-200 dark:border-[#2A313C] bg-slate-100 dark:bg-[#1C222B] flex items-center justify-center">
                  <m.icon className="w-4 h-4 text-slate-400 dark:text-slate-600" />
                </div>
                <div className="flex items-center justify-between w-full">
                  <span className="text-xs font-medium text-slate-400 dark:text-slate-500 truncate">
                    {m.title}
                  </span>
                  <Lock className="w-3 h-3 text-slate-400 dark:text-slate-600 flex-shrink-0" />
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* ── Dashboard Widgets ──────────────────────────────────────── */}
      <section>
        <h2 className="text-[10px] font-mono font-bold text-slate-400 dark:text-slate-500 uppercase tracking-widest mb-3">
          Telemetry & Command Dashboard
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          
          {/* Widget: Operational Health */}
          <div className="border border-slate-200 dark:border-[#1E293B] bg-white dark:bg-[#151A21]/40 rounded-[3px] p-5 flex flex-col sm:col-span-2 lg:col-span-2">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <HeartPulse className="w-4 h-4 text-orange-500" />
                <h3 className="text-xs font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wide">
                  Operational Health
                </h3>
              </div>
              <span className="text-[9px] font-mono text-[#22C55E] bg-[#22C55E]/10 border border-[#22C55E]/20 px-1.5 py-0.5 rounded-[2px]">
                LIVE FEED
              </span>
            </div>

            <div className="grid grid-cols-2 gap-4 mb-4">
              <div className="border border-slate-100 dark:border-[#1C222B] bg-slate-50/50 dark:bg-[#1C222B]/40 p-3 rounded-[3px] select-text">
                <span className="text-[10px] font-mono text-slate-400 dark:text-slate-500 uppercase">Grid Frequency</span>
                <div className="text-lg font-bold font-mono text-slate-800 dark:text-[#F8FAFC] mt-0.5">59.982 Hz</div>
                <div className="text-[9px] text-emerald-500 font-mono mt-0.5">▲ +0.002 (Nominal)</div>
              </div>
              <div className="border border-slate-100 dark:border-[#1C222B] bg-slate-50/50 dark:bg-[#1C222B]/40 p-3 rounded-[3px] select-text">
                <span className="text-[10px] font-mono text-slate-400 dark:text-slate-500 uppercase">Active Grid Load</span>
                <div className="text-lg font-bold font-mono text-slate-800 dark:text-[#F8FAFC] mt-0.5">1,424.8 MW</div>
                <div className="text-[9px] text-slate-400 dark:text-slate-500 font-mono mt-0.5">/ 2,000 MW Limit</div>
              </div>
            </div>

            {/* Load Flow SVG Sparkline Visualizer */}
            <div className="flex-1 min-h-[90px] border border-slate-100 dark:border-[#1E293B] bg-slate-50/20 dark:bg-[#0F1318]/40 rounded-[2px] p-3 flex flex-col justify-between">
              <div className="flex justify-between items-center text-[9px] font-mono text-slate-400 dark:text-slate-500">
                <span>ACTIVE POWER DEMAND GRADIENT</span>
                <span>LAST 60 MIN</span>
              </div>
              <div className="w-full h-12 flex items-end">
                <svg className="w-full h-full overflow-visible" viewBox="0 0 400 48" preserveAspectRatio="none">
                  <defs>
                    <linearGradient id="grid-grad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#FF7A1A" stopOpacity="0.25" />
                      <stop offset="100%" stopColor="#FF7A1A" stopOpacity="0" />
                    </linearGradient>
                  </defs>
                  <path
                    d="M0,32 Q25,28 50,38 T100,24 T150,34 T200,16 T250,28 T300,10 T350,22 T400,14"
                    fill="none"
                    stroke="#FF7A1A"
                    strokeWidth="1.5"
                    strokeLinecap="round"
                  />
                  <path
                    d="M0,32 Q25,28 50,38 T100,24 T150,34 T200,16 T250,28 T300,10 T350,22 T400,14 L400,48 L0,48 Z"
                    fill="url(#grid-grad)"
                  />
                </svg>
              </div>
              <div className="flex justify-between text-[8px] font-mono text-slate-400 dark:text-slate-600 border-t border-slate-100 dark:border-[#1E293B] pt-1">
                <span>60m ago</span>
                <span>30m ago</span>
                <span>Now</span>
              </div>
            </div>
          </div>

          {/* Widget: Recent Events */}
          <div className="border border-slate-200 dark:border-[#1E293B] bg-white dark:bg-[#151A21]/40 rounded-[3px] p-5 flex flex-col sm:col-span-1 lg:col-span-1">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <Clock className="w-4 h-4 text-violet-500" />
                <h3 className="text-xs font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wide">
                  Recent Events
                </h3>
              </div>
              <span className="text-[9px] font-mono text-slate-400 dark:text-slate-600">CIP-LOGS</span>
            </div>

            <div className="flex-1 flex flex-col justify-between space-y-3 font-mono text-[10px] select-text">
              <div className="flex gap-2.5 items-start border-l border-emerald-500/30 pl-2.5 py-0.5">
                <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 mt-1 flex-shrink-0" />
                <div className="flex-1">
                  <div className="text-slate-400 dark:text-slate-500 text-[8px]">15:18:42 // SYS.HEALTH</div>
                  <div className="text-slate-800 dark:text-slate-300 font-medium">Feeder Reno-1A nominal</div>
                </div>
              </div>
              <div className="flex gap-2.5 items-start border-l border-blue-500/30 pl-2.5 py-0.5">
                <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-1 flex-shrink-0" />
                <div className="flex-1">
                  <div className="text-slate-400 dark:text-slate-500 text-[8px]">15:15:02 // POLICY.ENGINE</div>
                  <div className="text-slate-800 dark:text-slate-300 font-medium">Rules verification compilation success</div>
                </div>
              </div>
              <div className="flex gap-2.5 items-start border-l border-[#FF7A1A]/30 pl-2.5 py-0.5">
                <div className="w-1.5 h-1.5 rounded-full bg-[#FF7A1A] mt-1 flex-shrink-0" />
                <div className="flex-1">
                  <div className="text-slate-400 dark:text-slate-500 text-[8px]">15:02:11 // AGENT.NEGO</div>
                  <div className="text-slate-800 dark:text-slate-300 font-medium">Voltage sag mitigated in 340ms</div>
                </div>
              </div>
            </div>
          </div>

          {/* Widget: Grid Map */}
          <div className="border border-slate-200 dark:border-[#1E293B] bg-white dark:bg-[#151A21]/40 rounded-[3px] p-5 flex flex-col sm:col-span-2 lg:col-span-2">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <Map className="w-4 h-4 text-cyan-500" />
                <h3 className="text-xs font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wide">
                  Topology Overview
                </h3>
              </div>
              <span className="text-[9px] font-mono text-slate-400 dark:text-slate-600">SCHEMATIC CANVAS</span>
            </div>

            <div className="flex-1 min-h-[140px] border border-slate-100 dark:border-[#1E293B] bg-[#0F1318] rounded-[2px] p-4 flex flex-col justify-center items-center relative overflow-hidden select-none">
              {/* Topological Canvas Vector */}
              <svg className="w-full max-w-sm h-28 overflow-visible" viewBox="0 0 300 100">
                {/* Node Sierra */}
                <circle cx="50" cy="50" r="6" fill="#22C55E" className="animate-pulse" />
                <text x="50" y="36" fill="#F8FAFC" fontSize="8" fontFamily="monospace" textAnchor="middle">SIERRA_SUB</text>
                
                {/* Node Reno */}
                <circle cx="150" cy="20" r="6" fill="#FF7A1A" />
                <text x="150" y="34" fill="#F8FAFC" fontSize="8" fontFamily="monospace" textAnchor="middle">RENO_FEED_1</text>
                
                {/* Node Tahoe */}
                <circle cx="250" cy="50" r="6" fill="#22C55E" />
                <text x="250" y="36" fill="#F8FAFC" fontSize="8" fontFamily="monospace" textAnchor="middle">TAHOE_BATTERY</text>

                {/* Connection lines */}
                <line x1="56" y1="50" x2="144" y2="22" stroke="#FF7A1A" strokeWidth="1" strokeDasharray="3,3" />
                <line x1="156" y1="22" x2="244" y2="48" stroke="#22C55E" strokeWidth="1" />
                <line x1="56" y1="50" x2="244" y2="50" stroke="#64748B" strokeWidth="0.5" />
              </svg>
              <div className="absolute bottom-2 left-2 text-[8px] font-mono text-[#64748B]">
                GREEN = COMPLIANT // ORANGE = AUTO-RESTORATION ACTIVE
              </div>
            </div>
          </div>

          {/* Widget: AI Recommendations */}
          <div className="border border-slate-200 dark:border-[#1E293B] bg-white dark:bg-[#151A21]/40 rounded-[3px] p-5 flex flex-col sm:col-span-1 lg:col-span-1">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <Lightbulb className="w-4 h-4 text-amber-500" />
                <h3 className="text-xs font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wide">
                  AI Recommendations
                </h3>
              </div>
              <span className="text-[9px] font-mono text-[#FFA940] bg-[#FFA940]/10 border border-[#FFA940]/20 px-1.5 py-0.5 rounded-[2px]">
                ACTIONABLE
              </span>
            </div>

            <div className="flex-1 flex flex-col justify-between">
              <div className="border border-[#FFA940]/20 bg-[#FFA940]/5 rounded-[3px] p-3 space-y-2 select-text">
                <div className="text-[10px] font-mono font-bold text-[#FFA940] uppercase flex items-center gap-1.5">
                  <Activity className="w-3.5 h-3.5" />
                  Volt-VAR Optimization
                </div>
                <p className="text-[11px] text-slate-600 dark:text-slate-300 leading-relaxed font-sans">
                  Autonomously curtail Tahoe battery discharge by 12MW to stabilize Sierra feeder frequency deviation.
                </p>
              </div>

              <div className="mt-3">
                {checkPermission("policies:view") ? (
                  <Link
                    to="/policy-engine"
                    className="w-full flex items-center justify-center gap-1 py-1.5 rounded-[2px] bg-[#1C222B] hover:bg-[#2A313C] border border-[#2A313C] text-[10px] font-semibold text-slate-200 hover:text-white transition-colors"
                  >
                    Review Boundary Policies
                    <ArrowUpRight className="w-3 h-3" />
                  </Link>
                ) : (
                  <div className="w-full flex items-center justify-center gap-2 py-1.5 rounded-[2px] bg-[#0F1318] border border-[#2A313C]/40 text-[9px] font-mono text-slate-500 cursor-not-allowed">
                    <Lock className="w-3 h-3" />
                    Operator clearance required to review
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Widget: Active Policies */}
          <div className="border border-slate-200 dark:border-[#1E293B] bg-white dark:bg-[#151A21]/40 rounded-[3px] p-5 flex flex-col sm:col-span-1 lg:col-span-1">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <ShieldCheck className="w-4 h-4 text-emerald-500" />
                <h3 className="text-xs font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wide">
                  Active Boundaries
                </h3>
              </div>
              <span className="text-[9px] font-mono text-slate-400 dark:text-slate-600">NERC-COMPLIANT</span>
            </div>

            <div className="flex-1 flex flex-col justify-between select-text">
              <div className="space-y-2.5 font-mono text-[10px]">
                <div className="flex justify-between items-center border-b border-slate-100 dark:border-[#1E293B] pb-1.5">
                  <span className="font-semibold text-slate-700 dark:text-slate-300">PRC-024-2 (Ride-Through)</span>
                  <span className="text-[8px] text-emerald-500 font-bold">ACTIVE</span>
                </div>
                <div className="flex justify-between items-center border-b border-slate-100 dark:border-[#1E293B] pb-1.5">
                  <span className="font-semibold text-slate-700 dark:text-slate-300">CIP-002 (Asset Verify)</span>
                  <span className="text-[8px] text-emerald-500 font-bold">ACTIVE</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="font-semibold text-slate-700 dark:text-slate-300">VAR-002 (Reactive Power)</span>
                  <span className="text-[8px] text-emerald-500 font-bold">ACTIVE</span>
                </div>
              </div>

              <div className="mt-3">
                {checkPermission("policies:view") ? (
                  <Link
                    to="/policy-engine"
                    className="w-full flex items-center justify-center gap-1 py-1.5 rounded-[2px] bg-[#1C222B] hover:bg-[#2A313C] border border-[#2A313C] text-[10px] font-semibold text-slate-200 hover:text-white transition-colors"
                  >
                    View Policy Code
                    <ArrowUpRight className="w-3 h-3" />
                  </Link>
                ) : (
                  <div className="w-full flex items-center justify-center gap-2 py-1.5 rounded-[2px] bg-[#0F1318] border border-[#2A313C]/40 text-[9px] font-mono text-slate-500 cursor-not-allowed">
                    <Lock className="w-3 h-3" />
                    Read-only clearance active
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Widget: Alerts */}
          <div className="border border-slate-200 dark:border-[#1E293B] bg-white dark:bg-[#151A21]/40 rounded-[3px] p-5 flex flex-col sm:col-span-1 lg:col-span-1">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <AlertTriangle className="w-4 h-4 text-emerald-500" />
                <h3 className="text-xs font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wide">
                  Active Alarms
                </h3>
              </div>
              <span className="text-[9px] font-mono text-slate-400 dark:text-slate-600">ALARMS</span>
            </div>

            <div className="flex-1 flex flex-col justify-center items-center py-4 select-text">
              <div className="w-9 h-9 rounded-full bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center mb-3">
                <CheckCircle2 className="w-4 h-4 text-emerald-500 animate-pulse" />
              </div>
              <div className="text-center">
                <h4 className="text-[11px] font-mono font-bold text-emerald-500 uppercase">Grid Stable</h4>
                <p className="text-[10px] text-slate-400 dark:text-slate-500 mt-1">
                  0 active grid alarms or policy breaches detected in local perimeter.
                </p>
              </div>
            </div>
          </div>

        </div>
      </section>
    </div>
  );
}

