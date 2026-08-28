import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi } from "vitest";
import { DecodeButton } from "../components/DecodeButton.jsx";

describe("DecodeButton", () => {
    it("calls decodeDna when clicked", async () => {
        const decodeDna = vi.fn();
        const user = userEvent.setup();

        render(
            <DecodeButton
                loading={ false }
                decodeDna={ decodeDna }
            />
        );

        await user.click(screen.getByRole("button", { name: "Decode" }));

        expect(decodeDna).toHaveBeenCalledOnce();
    })

    it("disables the button while loading", () => {
        const decodeDna = vi.fn();

        render(
            <DecodeButton
                loading={ true }
                decodeDna={ decodeDna }
            />
        );

        const button = screen.getByRole("button", { name: "Decoding..." });

        expect(button).toBeDisabled();
    });
});