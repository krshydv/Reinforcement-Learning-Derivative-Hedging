"use client"
import { usePortfolio } from "../../lib/queries"
import { StatCard } from "../../components/ui/Stat"

export default function PortfolioPage() {
  const portfolio = usePortfolio()
  return (
    <div className="glass rounded-2xl p-6">
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard label="Net Exposure" value={portfolio.data?.netExposure ?? 0} />
        <StatCard label="Gross Exposure" value={portfolio.data?.grossExposure ?? 0} />
        <StatCard label="Hedge Ratio" value={portfolio.data?.hedgeRatio ?? 0} />
        <StatCard label="Positions" value={portfolio.data?.positions?.length ?? 0} />
      </div>
      <div className="mt-6 overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-slate-400 text-left">
              <th className="py-2">Symbol</th>
              <th className="py-2">Quantity</th>
              <th className="py-2">Avg Price</th>
              <th className="py-2">Delta</th>
              <th className="py-2">Gamma</th>
            </tr>
          </thead>
          <tbody>
            {(portfolio.data?.positions ?? []).map(position => (
              <tr key={position.symbol} className="border-t border-slate-800">
                <td className="py-3">{position.symbol}</td>
                <td className="py-3">{position.quantity}</td>
                <td className="py-3">{position.avgPrice}</td>
                <td className="py-3">{position.delta}</td>
                <td className="py-3">{position.gamma}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
