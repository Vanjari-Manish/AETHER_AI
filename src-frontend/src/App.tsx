import { Suspense, lazy } from "react";
import { HashRouter, Routes, Route } from "react-router-dom";
import { ThemeProvider } from "@/context/ThemeContext";
import { AuthProvider } from "@/context/AuthContext";
import { TelemetryProvider } from "@/context/TelemetryContext";
import { ErrorBoundary } from "@/core/ErrorBoundary";
import { Layout } from "@/core/Layout";
import { LoadingPlaceholder } from "@/core/LoadingPlaceholder";
import { NotFound } from "@/core/NotFound";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { PublicRoute } from "@/components/PublicRoute";
import { PermissionGuard } from "@/components/PermissionGuard";
import { ShieldCheck } from "lucide-react";

// Grid Policy Orchestrator (GPO) Application Core Router (Phase 2.5 Rebuild)
// Path: src-frontend/src/App.tsx

const Home = lazy(() => import("@/routes/Home"));
const Login = lazy(() => import("@/routes/Login"));
const Register = lazy(() => import("@/routes/Register"));
const Unauthorized = lazy(() => import("@/routes/Unauthorized"));
const GridOverview = lazy(() => import("@/routes/GridOverview"));
const AssetWorkspace = lazy(() => import("@/assets/AssetWorkspace"));

// Reusable technical placeholder page for restricted modules
function PlaceholderPage({ title, permission }: { title: string; permission: string }) {
  return (
    <div className="space-y-6 py-2 select-text">
      <div>
        <p className="text-[10px] font-mono text-slate-400 dark:text-slate-500 uppercase tracking-widest mb-1.5">
          Clearance Authorized // {permission}
        </p>
        <h1 className="font-heading text-xl sm:text-2xl font-bold tracking-tight text-slate-900 dark:text-[#F8FAFC]">
          {title}
        </h1>
        <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
          This system module is fully configured under your current clearance permissions.
        </p>
      </div>

      <div className="border border-dashed border-slate-200 dark:border-[#2A313C] rounded-[4px] p-12 text-center">
        <div className="w-10 h-10 mx-auto rounded-full bg-slate-100 dark:bg-[#1C222B] border border-slate-200 dark:border-[#2A313C] flex items-center justify-center mb-4">
          <ShieldCheck className="w-5 h-5 text-emerald-500" />
        </div>
        <p className="text-xs text-slate-400 dark:text-slate-500 font-mono mb-2">
          [SYS.MODULE-STANDBY]
        </p>
        <p className="text-sm text-slate-500 dark:text-slate-400 max-w-sm mx-auto leading-relaxed">
          Operational telemetry and dashboard controls for {title} will compile on physical link activation.
        </p>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider>
        <AuthProvider>
          <TelemetryProvider>
            <HashRouter>
              <Suspense fallback={<LoadingPlaceholder />}>
                <Routes>
                {/* Public Auth Routes */}
                <Route
                  path="/login"
                  element={
                    <PublicRoute>
                      <Login />
                    </PublicRoute>
                  }
                />
                <Route
                  path="/register"
                  element={
                    <PublicRoute>
                      <Register />
                    </PublicRoute>
                  }
                />

                {/* Protected Application Routes */}
                <Route
                  path="/"
                  element={
                    <ProtectedRoute>
                      <PermissionGuard requiredPermission="dashboard:view">
                        <Layout>
                          <Home />
                        </Layout>
                      </PermissionGuard>
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/grid-overview"
                  element={
                    <ProtectedRoute>
                      <PermissionGuard requiredPermission="grid:view">
                        <Layout>
                          <GridOverview />
                        </Layout>
                      </PermissionGuard>
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/assets"
                  element={
                    <ProtectedRoute>
                      <PermissionGuard requiredPermission="assets:view">
                        <Layout>
                          <AssetWorkspace />
                        </Layout>
                      </PermissionGuard>
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/policy-engine"
                  element={
                    <ProtectedRoute>
                      <PermissionGuard requiredPermission="policies:view">
                        <Layout>
                          <PlaceholderPage title="Policy Engine" permission="policies:view" />
                        </Layout>
                      </PermissionGuard>
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/analytics"
                  element={
                    <ProtectedRoute>
                      <PermissionGuard requiredPermission="analytics:view">
                        <Layout>
                          <PlaceholderPage title="Analytics" permission="analytics:view" />
                        </Layout>
                      </PermissionGuard>
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/reports"
                  element={
                    <ProtectedRoute>
                      <PermissionGuard requiredPermission="reports:view">
                        <Layout>
                          <PlaceholderPage title="Reports" permission="reports:view" />
                        </Layout>
                      </PermissionGuard>
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/settings"
                  element={
                    <ProtectedRoute>
                      <PermissionGuard requiredPermission="settings:view">
                        <Layout>
                          <PlaceholderPage title="Settings" permission="settings:view" />
                        </Layout>
                      </PermissionGuard>
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/admin"
                  element={
                    <ProtectedRoute>
                      <PermissionGuard requiredPermission="admin:view">
                        <Layout>
                          <PlaceholderPage title="Administration" permission="admin:view" />
                        </Layout>
                      </PermissionGuard>
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/unauthorized"
                  element={
                    <ProtectedRoute>
                      <Layout>
                        <Unauthorized />
                      </Layout>
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="*"
                  element={
                    <ProtectedRoute>
                      <Layout>
                        <NotFound />
                      </Layout>
                    </ProtectedRoute>
                  }
                />
              </Routes>
            </Suspense>
          </HashRouter>
          </TelemetryProvider>
        </AuthProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
}
