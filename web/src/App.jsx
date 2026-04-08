import MapView from "./components/MapView";

export default function App() {
    return (
        <div className="min-h-screen bg-white text-slate-900">
            <header className="border-b border-slate-200 p-4">
                <h1 className="text-2xl font-bold">Ethnicities of Central Asia</h1>
                <p className="mt-1 text-sm text-slate-600">
                    Census-based regional ethnicity map
                </p>
            </header>

            <main className="grid grid-cols-1 lg:grid-cols-[320px_1fr]">
                <aside className="border-r border-slate-200 p-4">
                    <h2 className="font-semibold">Controls</h2>
                    <p className="mt-2 text-sm text-slate-600">
                        Filters, legend, and selected-region details go here.
                    </p>
                </aside>

                <section className="h-[calc(100vh-81px)]">
                    <MapView />
                </section>
            </main>
        </div>
    );
}