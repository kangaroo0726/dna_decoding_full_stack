import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi, afterEach } from "vitest";
import userEvent from "@testing-library/user-event";
import App from "../App.jsx";

describe("App", () => {
	it("renders the decoder interface", () => {
		render(<App />);

		expect(screen.getByRole("heading", { name: "DNA Decoder" })).toBeInTheDocument();
		expect(screen.getByRole("textbox", { name: "Sequence" })).toBeInTheDocument();
		expect(screen.getByRole("button", { name: "Decode" })).toBeInTheDocument();
		expect(screen.getByLabelText("Converted")).toBeInTheDocument();
		expect(screen.getByLabelText("Proteins")).toBeInTheDocument();
	});

    it("decodes a sequence and displays the results", async () => {
    const user = userEvent.setup();

    vi.stubGlobal(
        "fetch",
        vi.fn(() =>
            Promise.resolve({
                ok: true,
                json: () =>
                    Promise.resolve({
                        converted: "AUGUAA",
                        proteins: ["methionine", "stop"],
                    }),
            })
        )
    );

    render(<App />);

    const input = screen.getByRole("textbox", {
        name: "Sequence"
    });

    await user.type(input, "AUGUAA");
    await user.click(
        screen.getByRole("button", { name: "Decode" })
    );

    expect(await screen.findByLabelText("Converted")).toHaveValue("AUGUAA");
    expect(await screen.findByLabelText("Proteins")).toHaveValue("methionine, stop");
    });

    it("displays an API error", async () => {
        const user = userEvent.setup();

        vi.stubGlobal(
            "fetch",
            vi.fn(() =>
                Promise.resolve({
                    ok: false,
                    json: () => Promise.resolve({ detail: "Error: Methionine not found" }),
                })
            )
        );

        render(<App />);

        await user.click(screen.getByRole("button", { name: "Decode" }));

        expect(await screen.findByLabelText("Converted")).toHaveValue("Error: Methionine not found");
        expect(await screen.findByLabelText("Proteins")).toHaveValue("Error: Methionine not found");
    });

    it("handles a connection failure", async () => {
        const user = userEvent.setup();

        vi.stubGlobal("fetch", vi.fn(() => Promise.reject(new Error("Network error"))));

        render(<App />);

        await user.click(screen.getByRole("button", { name: "Decode" }));

        expect(await screen.findByLabelText("Converted")).toHaveValue("Unable to connect to the server.");
        expect(await screen.findByLabelText("Proteins")).toHaveValue("Unable to connect to the server.");
    });

    it("shows the loading state while decoding", async () => {
        const user = userEvent.setup();
        let resolveRequest;
        const pendingRequest = new Promise((resolve) => {
            resolveRequest = resolve;
        });

        vi.stubGlobal("fetch", vi.fn(() => pendingRequest));

        render(<App />);

        await user.click(screen.getByRole("button", { name: "Decode" }));

        const button = screen.getByRole("button", { name: "Decoding..." });
        expect(button).toBeDisabled();

        resolveRequest({
            ok: true,
            json: () => Promise.resolve({ converted: "", proteins: [] }),
        });
        expect(await screen.findByRole("button", { name: "Decode" })).not.toBeDisabled();
    });

    afterEach(() => {
    vi.restoreAllMocks();
    });
});
