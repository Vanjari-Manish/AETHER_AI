import { ReactNode, useEffect } from "react";
import { useTheme } from "../context/ThemeContext";
import {
  LayoutDashboard,
  Network,
  Building2,
  Cable,
  Shield,
  Box,
  Brain,
  BarChart3,
  FileText,
  Bell,
  Settings,
  Sun,
  Moon,
  ShieldCheck,
  Activity,
  Terminal,
} from "lucide-react";

interface LayoutProps {
  children: ReactNode;
}

export function Layout({ children }: LayoutProps) {
  const { theme, toggleTheme } = useTheme();

  useEffect(() => {
    document.title = "Grid Policy Orchestrator (GPO)";

    const viewportMeta = document.querySelector("meta[name='viewport']");
    if (viewportMeta) {
      viewportMeta.setAttribute(
        "content",
        "width=device-width, initial-scale=1.0, maximum-scale=5.0"
      );
    }
  }, []);

  const navItems = [
    { label: "Grid Overview", icon: LayoutDashboard, active: true },
    { label: "Grid Assets", icon: Network },
    { label: "Substations", icon: Building2 },
    { label: "Transmission Network", icon: Cable },
    { label: "Policy Engine", icon: Shield },
    { label: "Digital Twin", icon: Box },
    { label: "AI Intelligence", icon: Brain },
    { label: "Analytics", icon: BarChart3 },
    { label: "Reports", icon: FileText },
    { label: "Alerts", icon: Bell },
    { label: "Settings", icon: Settings },
  ];

  return (
    <div
      className={`min-h-screen flex flex-col font-sans antialiased select-none tracking-[-0.01em] transition-colors duration-200 ${
        theme === "dark" ? "bg-[#0B0E13] text-[#F8FAFC]" : "bg-slate-50 text-[#1E293B]"
      }`}
    >
      {/* Enterprise Header */}
      <header className="h-14 border-b border-slate-200 dark:border-[#1E293B] bg-white/70 dark:bg-[#0B0E13]/70 backdrop-blur-md px-4 flex items-center justify-between sticky top-0 z-40">
        <div className="flex items-center gap-3">
          {/* Logo */}
          <div className="flex items-center justify-center w-8 h-8 rounded-[4px] bg-slate-100 dark:bg-[#151A21] border border-slate-200 dark:border-[#2A313C]">
            <svg
              className="w-5 h-5 text-orange-500 dark:text-[#FF7A1A]"
              viewBox="0 0 256 256"
              fill="currentColor"
            >
              <path d="M 256 256 L 128 256 L 0 128 L 128 128 Z M 256 128 L 128 128 L 0 0 L 128 0 Z" />
            </svg>
          </div>
          <span className="font-heading text-sm font-semibold uppercase tracking-wider text-slate-800 dark:text-[#F8FAFC]">
            Grid Policy Orchestrator
          </span>
          <div className="flex items-center gap-2 ml-4">
            <span className="px-2 py-0.5 rounded-[2px] text-[10px] font-mono font-medium border border-orange-500/20 bg-orange-500/10 text-orange-500">
              DEVELOPMENT
            </span>
            <span className="px-2 py-0.5 rounded-[2px] text-[10px] font-mono font-medium border border-slate-200 dark:border-[#1E293B] bg-slate-100 dark:bg-[#151A21] text-slate-600 dark:text-slate-400">
              v1.5.0
            </span>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {/* Notifications Placeholder */}
          <button
            className="w-8 h-8 rounded-full border border-slate-200 dark:border-[#1E293B] bg-white dark:bg-[#151A21] flex items-center justify-center text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-[#F8FAFC] transition-colors relative"
            title="Notifications"
          >
            <Bell className="w-4 h-4" />
            <span className="absolute -top-0.5 -right-0.5 w-2 h-2 rounded-full bg-orange-500" />
          </button>

          {/* Theme Switcher */}
          <button
            onClick={toggleTheme}
            className="w-8 h-8 rounded-full border border-slate-200 dark:border-[#1E293B] bg-white dark:bg-[#151A21] flex items-center justify-center text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-[#F8FAFC] transition-colors"
            title="Toggle theme mode"
          >
            {theme === "dark" ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
          </button>

          {/* User Placeholder */}
          <div className="flex items-center gap-2 pl-3 border-l border-slate-200 dark:border-[#1E293B]">
            <div className="w-7 h-7 rounded-full bg-orange-500/10 border border-orange-500/30 flex items-center justify-center text-xs font-mono font-semibold text-orange-500">
              GO
            </div>
            <div className="hidden sm:block text-left">
              <span className="block text-xs font-medium text-slate-700 dark:text-slate-300">
                Grid Operator
              </span>
              <span className="block text-[9px] font-mono text-slate-500 uppercase leading-none">
                Not Authenticated
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Container */}
      <div className="flex-1 flex min-h-0">
        {/* Sidebar Navigation */}
        <aside className="w-60 border-r border-slate-200 dark:border-[#1E293B] bg-white dark:bg-[#0B0E13]/40 flex flex-col justify-between hidden md:flex">
          <div className="p-3 space-y-0.5">
            <div className="px-3 py-2 mb-2">
              <span className="text-[9px] font-mono text-slate-400 dark:text-slate-500 uppercase tracking-widest">
                Operations
              </span>
            </div>
            {navItems.map((item) => (
              <div
                key={item.label}
                className={`flex items-center gap-3 px-3 py-2 rounded-[4px] text-xs font-medium cursor-not-allowed transition-all ${
                  item.active
                    ? "bg-slate-100 dark:bg-[#151A21] text-orange-500 dark:text-[#FF7A1A] border border-slate-200/50 dark:border-[#2A313C]/40"
                    : "text-slate-600 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200"
                }`}
              >
                <item.icon className="w-4 h-4 flex-shrink-0" />
                <span>{item.label}</span>
              </div>
            ))}
          </div>

          {/* Security Domain Tag */}
          <div className="p-4 border-t border-slate-200 dark:border-[#1E293B] bg-slate-50/50 dark:bg-[#07090C]/20">
            <span className="block text-[9px] font-mono text-slate-500 uppercase tracking-wider">
              Security Domain
            </span>
            <span className="block text-[11px] font-semibold mt-1 text-slate-800 dark:text-slate-200 flex items-center gap-1.5">
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-500" />
              NERC CIP-002 — CIP-014
            </span>
          </div>
        </aside>

        {/* Content Workspace */}
        <main className="flex-1 overflow-y-auto bg-slate-50/30 dark:bg-[#07090C]/30 flex flex-col">
          <div className="flex-1 w-full mx-auto max-w-[1400px] p-6 sm:p-8">{children}</div>
        </main>
      </div>

      {/* Bottom Status Bar */}
      <footer className="h-7 border-t border-slate-200 dark:border-[#1E293B] bg-white dark:bg-[#0B0E13] px-4 flex items-center justify-between text-[10px] font-mono text-slate-500 dark:text-slate-400 tracking-wider">
        <div className="flex items-center gap-4">
          <span className="flex items-center gap-1.5 text-emerald-600 dark:text-emerald-500 font-semibold">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
            SYSTEM COMPLIANCE: NERC-CIP ACTIVE
          </span>
          <span className="hidden sm:inline border-l border-slate-200 dark:border-[#1E293B] pl-4">
            SECURE SESSION // TLS 1.3
          </span>
        </div>
        <div className="flex items-center gap-4">
          <span className="flex items-center gap-1">
            <Activity className="w-3.5 h-3.5" />
            LATENCY: 12ms
          </span>
          <span className="flex items-center gap-1">
            <Terminal className="w-3.5 h-3.5" />
            SIMULATION ENGINE: STANDBY
          </span>
        </div>
      </footer>
    </div>
  );
}

export default Layout;
