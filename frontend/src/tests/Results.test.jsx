import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { Results } from "../components/Results.jsx"

describe("Results", () => {
    it("displays the converted sequence", () => {
        render(<Results
            converted="AUGUAA"
            proteins="methionine, stop"
            />
        );
    

        expect(screen.getByLabelText("Converted")).toHaveValue("AUGUAA");
    });

    it("displays the translated proteins", () => {
        render(<Results
            converted="AUGUAA"
            proteins="methionine, stop"
            />
        );

        expect(screen.getByLabelText("Proteins")).toHaveValue("methionine, stop");
    })
});