import { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { fetchApplications } from "../api";

const STATUSES = ["saved", "applied", "interview", "offer", "rejected"];

export default function FunnelChart() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetchApplications().then((applications) => {
      const counts = STATUSES.map((status) => ({
        status,
        count: applications.filter((app) => app.status === status).length,
      }));
      setData(counts);
    });
  }, []);

  return (
    <div className="p-4">
      <h3 className="font-semibold mb-2">Application funnel</h3>
      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={data}>
          <XAxis dataKey="status" />
          <YAxis allowDecimals={false} />
          <Tooltip />
          <Bar dataKey="count" fill="#2563eb" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
