/**
 * @global
 * @interface Window
 * @property {ToastManager} toastManager - The singleton instance of ToastManager.
 */

/**
 * Configuration object defining the visual styles and content for different toast notification types.
 * Supports localization via the global `gettext` function if available.
 * @type {Object.<string, {bg: string, border: string, iconBg: string, iconColor: string, titleColor: string, textColor: string, progressColor: string, title: string, icon: string}>}
 */
const toastStyles = {
  success: {
    iconBg: "#10b981", // emerald-500
    titleColor: "#047857", // emerald-700
    progressColor: "#10b981",
    title: typeof gettext === "function" ? gettext("Success") : "Succès",
    icon: `<svg xmlns="http://www.w3.org/2000/svg" style="width:14px; height:14px; color:white;" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>`,
  },
  warning: {
    iconBg: "#f59e0b", // amber-500
    titleColor: "#b45309", // amber-700
    progressColor: "#f59e0b",
    title: typeof gettext === "function" ? gettext("Warning") : "Attention",
    icon: `<svg style="width:14px; height:14px; color:white;" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/>
                    <path d="M12 9v4"/>
                    <path d="M12 17h.01"/>
                </svg>`,
  },
  info: {
    iconBg: "#3b82f6", // blue-500
    titleColor: "#1d4ed8", // blue-700
    progressColor: "#3b82f6",
    title: typeof gettext === "function" ? gettext("Info") : "Info",
    icon: `<span style="font-size:12px; font-weight:bold; color:white;">i</span>`,
  },
  error: {
    iconBg: "#ef4444", // red-500
    titleColor: "#b91c1c", // red-700
    progressColor: "#ef4444",
    title: typeof gettext === "function" ? gettext("Error") : "Erreur",
    icon: `<svg xmlns="http://www.w3.org/2000/svg" style="width:14px; height:14px; color:white;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M18 6 6 18"/>
                    <path d="m6 6 12 12"/>
                </svg>`,
  },
};

/**
 * Manages the lifecycle, positioning, and rendering of toast notifications.
 * Handles responsive animations and automatic dismissal.
 */
class ToastManager {
  /**
   * Initializes the toast container and injects required CSS animations into the document head.
   * @constructor
   */
  constructor() {
    /** * Object holding the four corner containers.
     * @type {Object.<string, HTMLDivElement>}
     */
    this.containers = {};

    // Define the 4 standard corners
    const positions = ["top-left", "top-right", "bottom-left", "bottom-right"];

    positions.forEach((pos) => {
      const container = document.createElement("div");
      container.id = `toast-container-${pos}`;

      // Base classes: flex column
      container.className = "tm-container";

      this.containers[pos] = container;
      this.applyContainerStyles(container, pos);
      document.body.appendChild(container);
    });

    this.injectStyles();
  }

  create() {
    return new ToastBuilder(this);
  }

  /**
   * Applies specific CSS positioning to a container based on its corner.
   * @param {HTMLDivElement} container
   * @param {string} pos
   * @private
   */
  applyContainerStyles(container, pos) {
    const isMobile = window.innerWidth < 768;

    if (isMobile) {
      container.style.left = "50%";
      container.style.transform = "translateX(-50%)";
      if (pos.includes("top")) container.style.top = "1rem";
      else container.style.bottom = "1rem";

      // Hide containers that aren't the primary mobile ones to avoid overlap
      // Usually mobile only uses one "active" side (top or bottom)
    } else {
      const [y, x] = pos.split("-");
      container.style[y] = "1rem";
      container.style[x] = "1rem";
    }
  }

  injectStyles() {
    const styles = `
      .tm-container {
        position: fixed;
        z-index: 9999999;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        width: 100%;
        max-width: 350px;
        pointer-events: none;
        transition: all 0.4s;
      }
      @media (max-width: 768px) {
        .tm-container { max-width: 90vw; }
      }
      .tm-toast {
        pointer-events: auto;
        width: 100%;
        background: #ffffff;
        border: 1px solid #e5e7eb;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
        font-family: 'DM Sans', 'Montserrat', sans-serif;
      }
      .tm-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
      }
      .tm-icon-wrapper {
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 24px;
        height: 24px;
        flex-shrink: 0;
      }
      .tm-title {
        font-size: 1rem;
        font-weight: 600;
        margin: 0;
        line-height: 1.2;
      }
      .tm-message {
        color: #4b5563;
        font-size: 0.875rem;
        margin: 0.5rem 0 0 0;
        line-height: 1.5;
      }
      .tm-close-btn {
        background: transparent;
        border: none;
        color: #9ca3af;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        position: absolute;
        right: 0.5rem;
        top: 0.5rem;
        border-radius: 50%;
        width: 24px;
        height: 24px;
        padding: 0;
        transition: background 0.2s;
      }
      .tm-close-btn:hover {
        background: #f3f4f6;
        color: #374151;
      }
      .tm-progress-bar {
        position: absolute;
        bottom: 0;
        left: 0;
        height: 4px;
      }
      [id^="toast-container-"] > div { pointer-events: auto; }
      @keyframes slide-in-right { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
      @keyframes slide-out-right { from { transform: translateX(0); opacity: 1; } to { transform: translateX(100%); opacity: 0; } }
      @keyframes slide-in-left { from { transform: translateX(-100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
      @keyframes slide-out-left { from { transform: translateX(0); opacity: 1; } to { transform: translateX(-100%); opacity: 0; } }
      @keyframes slide-in-bottom { from { transform: translateY(100%); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
      @keyframes slide-out-bottom { from { transform: translateY(0); opacity: 1; } to { transform: translateY(100%); opacity: 0; } }
      @keyframes slide-in-top { from { transform: translateY(-100%); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
      @keyframes slide-out-top { from { transform: translateY(0); opacity: 1; } to { transform: translateY(-100%); opacity: 0; } }

      .animate-slide-in-right { animation: slide-in-right 0.3s ease-out forwards; }
      .animate-slide-out-right { animation: slide-out-right 0.3s ease-in forwards; }
      .animate-slide-in-left { animation: slide-in-left 0.3s ease-out forwards; }
      .animate-slide-out-left { animation: slide-out-left 0.3s ease-in forwards; }
      .animate-slide-in-bottom { animation: slide-in-bottom 0.3s ease-out forwards; }
      .animate-slide-out-bottom { animation: slide-out-bottom 0.3s ease-in forwards; }
      .animate-slide-in-top { animation: slide-in-top 0.3s ease-out forwards; }
      .animate-slide-out-top { animation: slide-out-top 0.3s ease-in forwards; }

      @keyframes progress { from { width: 100%; } to { width: 0%; } }
      .progress-bar-toast { animation: progress linear forwards; }
    `;
    const styleSheet = document.createElement("style");
    styleSheet.textContent = styles;
    document.head.appendChild(styleSheet);
  }

  /**
   * Creates and displays a new toast notification.
   * @param {string} message - The main content of the toast.
   * @param {'success'|'warning'|'info'|'error'} [type="info"] - The notification style type.
   * @param {'top-left'|'top-right'|'bottom-left'|'bottom-right'} [position="top-right"] - Screen corner position.
   * @param {number} [duration=4000] - Visibility time in milliseconds before automatic dismissal.
   * @param {string|null} icon - Optional custom icon HTML. If not provided, it will use the default icon based on the type.
   * @param {string|null} title - The title of the toast, if not provided it will use the default title based on the type.
   */
  showToast(
    message,
    type = "info",
    position = "top-right",
    duration = 4000,
    icon = null,
    title = null,
  ) {
    const style = toastStyles[type] || toastStyles.info;
    const targetContainer =
      this.containers[position] || this.containers["top-right"];

    const existingToastsCount = targetContainer.children.length;
    const staggerDelay = existingToastsCount * 100;

    const isMobile = window.innerWidth < 768;
    let slideIn, slideOut;

    if (isMobile) {
      slideIn = position.includes("top")
        ? "animate-slide-in-top"
        : "animate-slide-in-bottom";
      slideOut = position.includes("top")
        ? "animate-slide-out-top"
        : "animate-slide-out-bottom";
    } else {
      slideIn = position.includes("left")
        ? "animate-slide-in-left"
        : "animate-slide-in-right";
      slideOut = position.includes("left")
        ? "animate-slide-out-left"
        : "animate-slide-out-right";
    }

    const toast = document.createElement("div");
    toast.className = `tm-toast ${slideIn}`;

    toast.style.animationDelay = `${staggerDelay}ms`;
    // On cache le toast initialement pour éviter qu'il clignote avant l'animation
    toast.style.opacity = "0";
    toast.style.animationFillMode = "forwards";

    // Use a data attribute to store the out-animation for closeAllToasts logic
    toast.dataset.animateOut = slideOut;
    toast.dataset.animateIn = slideIn;

    toast.innerHTML = `
            <div class="tm-content">
                <div class="tm-header">
                    <div class="tm-icon-wrapper" style="background-color: ${style.iconBg};">
                        ${icon ?? style.icon}
                    </div>
                    <h2 class="tm-title" style="color: ${style.titleColor};">${title ?? style.title}</h2>
                </div>
                <p class="tm-message">${message}</p>
                <button class="tm-close-btn close-toast" style="animation-duration: ${duration}ms; animation-delay: ${staggerDelay}ms">
                    <svg xmlns="http://www.w3.org/2000/svg" style="width:14px; height:14px;" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>
            <div class="tm-progress-bar progress-bar-toast" style="background-color: ${style.progressColor}; animation-duration: ${duration}ms"></div>
        `;

    targetContainer.appendChild(toast);

    const removeToast = () => {
      if (!toast.classList.contains(slideOut)) {
        toast.style.animationDelay = "0ms";
        toast.classList.remove(slideIn);
        toast.classList.add(slideOut);
        toast.addEventListener("animationend", () => toast.remove(), {
          once: true,
        });
        setTimeout(() => toast.remove(), 400);
      }
    };

    toast.querySelector(".close-toast").onclick = removeToast;
    setTimeout(removeToast, duration + staggerDelay);
  }

  /**
   * Closes all toasts across all 4 containers.
   */
  closeAllToasts() {
    Object.values(this.containers).forEach((container) => {
      container.querySelectorAll("div[data-animate-out]").forEach((toast) => {
        const out = toast.dataset.animateOut;
        const inAnim = toast.dataset.animateIn;
        toast.classList.remove(inAnim);
        toast.classList.add(out);
        setTimeout(() => toast.remove(), 400);
      });
    });
  }
}

/**
 * Builder class for configuring and displaying toasts fluently.
 * @class
 */
class ToastBuilder {
  /**
   * @param {ToastManager} manager - The ToastManager instance.
   */
  constructor(manager) {
    this.manager = manager;
    this.config = {
      message: "",
      type: "info",
      position: "top-right",
      duration: 4000,
      icon: null,
      title: null,
    };
  }

  /**
   * Sets the toast message.
   * @param {string} message
   * @returns {ToastBuilder}
   */
  setMessage(message) {
    this.config.message = message;
    return this;
  }

  /**
   * Sets the toast type ('success', 'warning', 'info', 'error').
   * @param {'success'|'warning'|'info'|'error'} type
   * @returns {ToastBuilder}
   */
  setType(type) {
    this.config.type = type;
    return this;
  }

  /**
   * Sets the screen corner position.
   * @param {'top-left'|'top-right'|'bottom-left'|'bottom-right'} position
   * @returns {ToastBuilder}
   */
  setPosition(position) {
    this.config.position = position;
    return this;
  }

  /**
   * Sets the display duration in ms.
   * @param {number} duration
   * @returns {ToastBuilder}
   */
  setDuration(duration) {
    this.config.duration = duration;
    return this;
  }

  /**
   * Sets a custom title for the toast.
   * @param {string} title
   * @returns {ToastBuilder}
   */
  setTitle(title) {
    this.config.title = title;
    return this;
  }

  /**
   * Sets a custom HTML icon.
   * @param {string} icon
   * @returns {ToastBuilder}
   */
  setIcon(icon) {
    this.config.icon = icon;
    return this;
  }

  /**
   * Triggers the toast display via the manager.
   */
  show() {
    const { message, type, position, duration, icon, title } = this.config;
    this.manager.showToast(message, type, position, duration, icon, title);
  }
}

/** @type {ToastManager} */
const toastManager = new ToastManager();
/** @type {ToastManager} */
window.toastManager = toastManager;
