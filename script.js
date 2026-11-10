// P4: hide links only after JavaScript has installed the controls.
    (() => {
      const toggle = document.getElementById("menu-toggle");
      const navigation = document.getElementById("primary-navigation");
      const narrow = window.matchMedia("(max-width:680px)");
      const setOpen = (open) => {
        navigation.hidden = !open;
        toggle.setAttribute("aria-expanded", String(open));
      };
      const syncWidth = () => {
        const active = document.activeElement;
        toggle.hidden = !narrow.matches;
        setOpen(!narrow.matches);
        if (narrow.matches && navigation.contains(active)) toggle.focus();
        if (!narrow.matches && active === toggle) navigation.querySelector("a").focus();
      };
      toggle.addEventListener("click", () => setOpen(navigation.hidden));
      document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && narrow.matches && !navigation.hidden) {
          event.preventDefault();
          setOpen(false);
          toggle.focus();
        }
      });
      navigation.addEventListener("click", (event) => {
        const link = event.target.closest("a[href]");
        if (!link || !narrow.matches) return;
        const target = document.getElementById(link.hash.slice(1));
        if (!target) return;
        setOpen(false);
        const temporaryTabIndex = !target.hasAttribute("tabindex");
        if (temporaryTabIndex) {
          target.setAttribute("tabindex", "-1");
          target.addEventListener("blur", () => target.removeAttribute("tabindex"), {once:true});
        }
        target.focus({preventScroll:true});
      });
      narrow.addEventListener("change", syncWidth);
      syncWidth();
    })();

// P5: no transport, storage or logging; fail closed if JS is unavailable.
    (() => {
      const form = document.getElementById("demo-form");
      const name = document.getElementById("name");
      const email = document.getElementById("email");
      const status = document.getElementById("form-status");
      let attempted = false;
      const announce = (message) => {
        if (status.textContent !== message) status.textContent = message;
      };
      const validate = (field) => {
        let message = "";
        if (field === name && !field.value.trim()) message = "Введите имя: не только пробелы.";
        if (field === email) {
          if (field.validity.valueMissing) message = "Введите email для проверки.";
          else if (!field.validity.valid) message = "Введите корректный email, например demo@example.test.";
        }
        const error = document.getElementById(field.id + "-error");
        field.setAttribute("aria-invalid", String(Boolean(message)));
        error.textContent = message;
        error.hidden = !message;
        return !message;
      };
      form.addEventListener("submit", (event) => {
        event.preventDefault();
        attempted = true;
        const nameValid = validate(name);
        const emailValid = validate(email);
        if (!nameValid || !emailValid) {
          announce("Проверьте выделенные поля.");
          (nameValid ? email : name).focus();
          return;
        }
        announce("Проверка пройдена. Это демонстрация: данные никуда не отправлены");
      });
      for (const field of [name, email]) {
        field.addEventListener("input", () => {
          if (attempted) validate(field);
          announce("");
        });
      }
      // Reset visual errors and the validation attempt, not just input values.
      form.addEventListener("reset", () => {
        attempted = false;
        for (const field of [name, email]) {
          field.setAttribute("aria-invalid", "false");
          const error = document.getElementById(field.id + "-error");
          error.textContent = "";
          error.hidden = true;
        }
        announce("Поля очищены. Можно начать проверку заново.");
        name.focus();
      });
      document.getElementById("demo-reset").disabled = false;
      // Enable custom validation only after the safe submit listener is installed.
      form.noValidate = true;
      document.getElementById("demo-submit").disabled = false;
    })();
