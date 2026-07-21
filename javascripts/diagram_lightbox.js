document.addEventListener("DOMContentLoaded", () => {
    // 1. Create the Modal element and append it to body
    const modal = document.createElement("div");
    modal.className = "diagram-lightbox-modal";
    modal.innerHTML = `
        <div class="diagram-lightbox-content">
            <span class="diagram-lightbox-close">&times;</span>
            <div class="diagram-lightbox-target"></div>
        </div>
    `;
    document.body.appendChild(modal);

    const closeBtn = modal.querySelector(".diagram-lightbox-close");
    const targetContainer = modal.querySelector(".diagram-lightbox-target");

    // Close on clicking 'X'
    closeBtn.addEventListener("click", () => {
        modal.classList.remove("active");
    });

    // Close on clicking outside the content box
    modal.addEventListener("click", (e) => {
        if (e.target === modal) {
            modal.classList.remove("active");
        }
    });

    // Close on pressing Escape key
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && modal.classList.contains("active")) {
            modal.classList.remove("active");
        }
    });

    // 2. Locate all diagram wrappers and add the expand button & click event
    document.querySelectorAll(".diagram-outer-wrapper").forEach((wrapper) => {
        // Add hover expand button
        const btn = document.createElement("button");
        btn.className = "diagram-expand-btn";
        btn.innerHTML = "⛶ EXPAND";
        wrapper.appendChild(btn);

        // Click handler
        const openLightbox = () => {
            const mermaidDiv = wrapper.querySelector(".mermaid");
            if (mermaidDiv) {
                // Clone the mermaid div to keep the original in the document
                const clone = mermaidDiv.cloneNode(true);
                targetContainer.innerHTML = "";
                targetContainer.appendChild(clone);
                modal.classList.add("active");
            }
        };

        wrapper.addEventListener("click", (e) => {
            openLightbox();
        });
    });
});
