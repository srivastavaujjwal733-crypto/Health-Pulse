
(() => {
  "use strict";

  const API_URL = "http://127.0.0.1:8000/ai-chat";

  // Automatically load the shared chatbot stylesheet.
  if (!document.querySelector('link[data-healthpulse-chat-css]')) {
    const css = document.createElement("link");
    css.rel = "stylesheet";
    css.href = new URL("./chatbot.css", document.currentScript.src).href;
    css.dataset.healthpulseChatCss = "true";
    document.head.appendChild(css);
  }

  const fullPage = document.getElementById("healthpulse-chat-app");

  const welcomeMessage =
    "Namaste! Main HealthPulse AI hoon. Aap heart health, blood pressure, " +
    "cholesterol aur healthy lifestyle ke baare mein general questions pooch sakte hain.";

  function createChatMarkup() {
    return `
      <div class="hp-chat-header">
        <div class="hp-chat-avatar" aria-hidden="true">✚</div>
        <div class="hp-chat-heading">
          <strong>HealthPulse AI</strong>
          <small>Health education assistant</small>
        </div>
        ${fullPage ? "" : '<button class="hp-chat-close" type="button" aria-label="Close chat">×</button>'}
      </div>

      <div class="hp-chat-messages" role="log" aria-live="polite" aria-label="Chat messages"></div>

      <div class="hp-chat-suggestions">
        <button type="button" data-prompt="Heart ko healthy kaise rakhein?">Heart health</button>
        <button type="button" data-prompt="Blood pressure ke baare mein general information do.">Blood pressure</button>
        <button type="button" data-prompt="Healthy lifestyle ke liye daily habits batao.">Healthy habits</button>
      </div>

      <form class="hp-chat-form">
        <textarea class="hp-chat-input" rows="1" maxlength="1000"
          placeholder="Apna health question likhein..."
          aria-label="Your health question" required></textarea>
        <button class="hp-chat-send" type="submit" aria-label="Send message">➤</button>
      </form>

      <div class="hp-chat-disclaimer">
        General health education only, not a medical diagnosis. Emergency symptoms mein
        turant medical help lein.
      </div>
    `;
  }

  function initializeChat(panel) {
    panel.innerHTML = createChatMarkup();

    const messages = panel.querySelector(".hp-chat-messages");
    const form = panel.querySelector(".hp-chat-form");
    const input = panel.querySelector(".hp-chat-input");
    const sendButton = panel.querySelector(".hp-chat-send");

    function addMessage(text, who) {
      const message = document.createElement("div");
      message.className =
        "hp-message " + (who === "user" ? "hp-message-user" : "hp-message-bot");

      // Use textContent so API output is treated as text, not executable HTML.
      message.textContent = text;
      messages.appendChild(message);
      messages.scrollTop = messages.scrollHeight;
      return message;
    }

    addMessage(welcomeMessage, "bot");

    async function sendMessage(text) {
      const message = text.trim();
      if (!message || sendButton.disabled) return;

      addMessage(message, "user");
      input.value = "";
      sendButton.disabled = true;
      input.disabled = true;

      const loading = addMessage("HealthPulse AI jawab taiyar kar raha hai...", "bot");

      try {
        const response = await fetch(API_URL, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message })
        });

        const result = await response.json().catch(() => ({}));
        loading.remove();

        if (!response.ok) {
          throw new Error(
            result.detail || `Request failed (${response.status}).`
          );
        }

        if (!result.success || typeof result.reply !== "string") {
          throw new Error("AI se valid response nahi mila. Dobara try karein.");
        }

        addMessage(result.reply, "bot");
      } catch (error) {
        loading.remove();

        let helpText = error.message || "Unknown error";

        if (error instanceof TypeError) {
          helpText =
            "Backend se connect nahi ho pa raha. Check karein ki FastAPI " +
            "http://127.0.0.1:8000 par chal raha hai aur CORS configured hai.";
        }

        addMessage("Maaf kijiye, abhi jawab nahi mil saka. " + helpText, "bot");
      } finally {
        sendButton.disabled = false;
        input.disabled = false;
        input.focus();
      }
    }

    form.addEventListener("submit", (event) => {
      event.preventDefault();
      sendMessage(input.value);
    });

    panel.querySelectorAll("[data-prompt]").forEach((button) => {
      button.addEventListener("click", () => {
        sendMessage(button.dataset.prompt);
      });
    });

    input.addEventListener("keydown", (event) => {
      if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        form.requestSubmit();
      }
    });

    return {
      focus() {
        input.focus();
      }
    };
  }

  if (fullPage) {
    fullPage.classList.add("hp-full-chat");
    fullPage.innerHTML = `
      <div class="hp-full-container">
        <div class="hp-full-top">
          <div class="hp-brand">HEALTHPULSE</div>
          <a href="./index.html">← Back to Home</a>
        </div>
        <div class="hp-brand">YOUR HEALTH COMPANION</div>
        <h1 class="hp-full-title">Ask HealthPulse AI</h1>
        <p class="hp-full-subtitle">
          Understand heart health and healthy lifestyle topics in simple language.
          Ask a question below to get started.
        </p>
        <section class="hp-full-panel" aria-label="HealthPulse AI chat"></section>
      </div>
    `;

    initializeChat(fullPage.querySelector(".hp-full-panel"));
    return;
  }

  // Add a floating chatbot to existing pages.
  const launcher = document.createElement("button");
  launcher.type = "button";
  launcher.className = "hp-chat-launcher";
  launcher.textContent = "✚  Ask HealthPulse AI";
  launcher.setAttribute("aria-expanded", "false");
  launcher.setAttribute("aria-label", "Open HealthPulse AI chat");

  const panel = document.createElement("section");
  panel.className = "hp-chat-window";
  panel.hidden = true;
  panel.setAttribute("aria-label", "HealthPulse AI chat");

  document.body.append(launcher, panel);

  let chat = null;

  launcher.addEventListener("click", () => {
    panel.hidden = false;
    launcher.setAttribute("aria-expanded", "true");
    launcher.hidden = true;

    if (!chat) chat = initializeChat(panel);
    chat.focus();
  });

  panel.addEventListener("click", (event) => {
    if (event.target.closest(".hp-chat-close")) {
      panel.hidden = true;
      launcher.hidden = false;
      launcher.setAttribute("aria-expanded", "false");
      launcher.focus();
    }
  });
})();
