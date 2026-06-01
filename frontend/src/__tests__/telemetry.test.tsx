import React from "react"
import { render, screen } from "@testing-library/react"
import TelemetryPage from "../app/telemetry/page"

vi.mock("../hooks/useTelemetry", () => ({
  useTelemetryStream: () => undefined,
  useTelemetryChannel: () => ({ events: [], status: "connected" })
}))

test("renders telemetry console", () => {
  render(<TelemetryPage />)
  expect(screen.getByText(/Telemetry Console/i)).toBeInTheDocument()
})
