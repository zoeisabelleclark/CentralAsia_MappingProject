import React from "react";

export default function SidebarFooter() {
    return (
        <div
            style={{
                fontSize: "0.8rem",
                color: "#6b7280",
                lineHeight: 1.5,
            }}
        >
            <div style={{ marginBottom: "0.4rem" }}>
                Built by{" "}
                <a
                    href="https://zoeisabelleclark.com/"
                    target="_blank"
                    rel="noopener noreferrer"
                    style={{
                        color: "#111827",
                        textDecoration: "none",
                        fontWeight: 600,
                    }}
                >
                    Zoë Clark
                </a>
            </div>

            <div>
                <a
                    href="https://github.com/zoeisabelleclark/CentralAsia_MappingProject"
                    target="_blank"
                    rel="noopener noreferrer"
                    style={{
                        color: "#6b7280",
                        textDecoration: "none",
                    }}
                >
                    View source on GitHub →
                </a>
            </div>
        </div>
    );
}