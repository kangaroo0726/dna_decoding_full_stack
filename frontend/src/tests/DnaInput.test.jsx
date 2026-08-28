import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi } from "vitest";
import { DnaInput } from "../components/DnaInput.jsx";

describe("DnaInput", () => {
    it("updates the strand when user types", async () => {
        const user = userEvent.setup();
        const setStrand = vi.fn();
        const setStrandType = vi.fn();
        const setFiveToThree = vi.fn();

        render(
            <DnaInput
                strand=""
                setStrand={ setStrand }
                strandType="template"
                setStrandType={ setStrandType }
                fiveToThree={ false }
                setFiveToThree={ setFiveToThree }
            />
        );
        
        const input = screen.getByRole("textbox", {
            name: "Sequence"
        });

        await user.type(input, "AUG");

        expect(setStrand).toHaveBeenCalled();
    });

    it("updates the strand type when the user selects a different type", async () => {
    const user = userEvent.setup();

    const setStrand = vi.fn();
    const setStrandType = vi.fn();
    const setFiveToThree = vi.fn();

    render(
        <DnaInput
            strand=""
            setStrand={setStrand}
            strandType="template"
            setStrandType={setStrandType}
            fiveToThree={false}
            setFiveToThree={setFiveToThree}
        />
    );

    await user.selectOptions(
        screen.getByRole("combobox"),
        "mrna"
    );

    expect(setStrandType).toHaveBeenCalledWith("mrna");
});

    it("updates orientation when the user checks the checkbox", async () => {
        const user = userEvent.setup();

        const setStrand = vi.fn();
        const setStrandType = vi.fn();
        const setFiveToThree = vi.fn();

        render(
            <DnaInput
                strand=""
                setStrand={setStrand}
                strandType="template"
                setStrandType={setStrandType}
                fiveToThree={false}
                setFiveToThree={setFiveToThree}
            />
        );

        await user.click(
            screen.getByLabelText("Five to three")
        );

        expect(setFiveToThree).toHaveBeenCalledWith(true);
    });
});