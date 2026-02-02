import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from "chart.js"
import { Bar } from "react-chartjs-2"
import { useEffect, useMemo, useState } from "react"
import { useNavigate, useParams } from "react-router-dom"
import axios from "axios"
import { toast } from "react-toastify"

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend
)

type Dataset = {
  id: number
  total_count: number
  avg_flowrate: number
  avg_pressure: number
  avg_temperature: number
  type_distribution: Record<string, number>
}

export const Report = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const [dataset, setDataset] = useState<Dataset | null>(null)

  const headers = useMemo(() => {
    const token = localStorage.getItem("access_token")
    return { Authorization: `Bearer ${token}` }
  }, [])

  useEffect(() => {
    const fetchReport = async () => {
      try {
        const res = await axios.get(
          "http://127.0.0.1:8000/api/summary/",
          { headers }
        )

        const found = res.data.find((d: Dataset) => d.id === Number(id))
        if (!found) {
          toast.error("Report not found")
          navigate("/dashboard")
          return
        }

        setDataset(found)
      } catch {
        toast.error("Failed to load report")
        navigate("/dashboard")
      }
    }

    fetchReport()
  }, [headers, id, navigate])

  if (!dataset) {
    return (
      <div className="p-10 text-center text-gray-500">
        Loading report...
      </div>
    )
  }

  const chartData = {
    labels: Object.keys(dataset.type_distribution),
    datasets: [
      {
        label: "Equipment Count",
        data: Object.values(dataset.type_distribution),
        backgroundColor: "#2563eb",
      },
    ],
  }

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: { display: false },
    },
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8 space-y-8">
      {/* HEADER */}
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-800">
          Dataset Report #{dataset.id}
        </h1>

        <button
          onClick={() => navigate("/dashboard")}
          className="text-blue-600 hover:underline"
        >
          ← Back to Dashboard
        </button>
      </div>

      {/* STATS */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <StatCard title="Total Records" value={dataset.total_count} />
        <StatCard title="Avg Flowrate" value={dataset.avg_flowrate.toFixed(2)} />
        <StatCard title="Avg Pressure" value={dataset.avg_pressure.toFixed(2)} />
        <StatCard title="Avg Temperature" value={dataset.avg_temperature.toFixed(2)} />
      </div>

      {/* CHART */}
      <div className="bg-white rounded-xl shadow p-6">
        <h2 className="text-lg font-semibold mb-4">
          Equipment Type Distribution
        </h2>
        <Bar data={chartData} options={chartOptions} />
      </div>
    </div>
  )
}

const StatCard = ({
  title,
  value,
}: {
  title: string
  value: string | number
}) => (
  <div className="bg-white rounded-xl shadow p-6">
    <p className="text-sm text-gray-500">{title}</p>
    <p className="text-2xl font-bold mt-2">{value}</p>
  </div>
)
