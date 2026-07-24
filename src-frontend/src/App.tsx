import { Suspense, lazy } from "react";
import { HashRouter, Routes, Route } from "react-router-dom";
import { ThemeProvider } from "@/context/ThemeContext";
import { ErrorBoundary } from "@/core/ErrorBoundary";
import { Layout } from "@/core/Layout";
import { LoadingPlaceholder } from "@/core/LoadingPlaceholder";
import { NotFound } from "@/core/NotFound";

const Home = lazy(() => import("@/routes/Home"));

export default function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider>
        <HashRouter>
          <Layout>
            <Suspense fallback={<LoadingPlaceholder />}>
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="*" element={<NotFound />} />
              </Routes>
            </Suspense>
          </Layout>
        </HashRouter>
      </ThemeProvider>
    </ErrorBoundary>
  );
}
