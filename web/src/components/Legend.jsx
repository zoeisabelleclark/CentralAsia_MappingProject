import React from "react";

export default function Legend() {
    return (
        <div style={{
            position: "absolute",
            bottom: "20px",
            right: "20px",
            background: "white",
            padding: "10px",
            borderRadius: "8px",
            boxShadow: "0 2px 6px rgba(0,0,0,0.2)"
        }}>
            <div><strong>Dominant ethnicity (%)</strong></div>
            <div>75%+</div>
            <div>50–75%</div>
            <div>25–50%</div>
            <div>10–25%</div>
            <div>&lt;10%</div>
        </div>
    );
}