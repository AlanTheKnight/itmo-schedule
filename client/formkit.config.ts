import { generateClasses } from "@formkit/themes";
import { ru, en } from "@formkit/i18n";
import { defineFormKitConfig } from "@formkit/vue";

export default defineFormKitConfig({
  locales: { ru, en },
  locale: "en",
  config: {
    classes: generateClasses({
      global: {
        outer: "$reset form-group",
        input: "form-control",
        label: "form-label",
        messages: "list-unstyled small mb-0",
        message: "is-invalid",
        help: "form-text",
      },
      checkbox: {
        label: "form-check-label",
        wrapper: "checkbox-wrapper",
        inner: "form-check",
        input: "$reset form-check-input",
        legend: "$reset form-check-label",
      },
      select: {
        input: "$reset form-select",
      },
      radio: {
        label: "form-check-label",
        wrapper: "radio-wrapper",
        inner: "form-check",
        input: "$reset form-check-input",
        legend: "$reset form-check-label",
      },
      submit: {
        outer: "$reset mt-3 text-center",
        input: "$reset btn btn-outline-light px-4",
      },
    }),
  },
});
