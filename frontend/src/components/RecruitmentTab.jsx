import React, { useState, useEffect } from "react";
import {
  Users,
  Briefcase,
  BarChart2,
  Lightbulb,
  TrendingUp,
  Plus,
  Filter,
  Mail,
  User,
  Code,
  Brush,
  Sparkles,
  Megaphone,
} from "lucide-react";

const RecruitmentTab = () => {
  const [jobs, setJobs] = useState([]);
  const [candidates, setCandidates] = useState([]);

  useEffect(() => {
    // Dummy data for now (replace with your API fetch later)
    setJobs([
      { id: 1, title: "Senior Software Engineer", applications: 45, qualified: 8, icon: Code },
      { id: 2, title: "UX Designer", applications: 32, qualified: 12, icon: Brush },
      { id: 3, title: "Marketing Manager", applications: 28, qualified: 6, icon: Megaphone },
    ]);

    setCandidates([
      { id: 1, name: "user_01", role: "Frontend Developer", match: "95%" },
      { id: 2, name: "user_02", role: "Backend Developer", match: "88%" },
      { id: 3, name: "user_03", role: "Manager", match: "76%" },
    ]);
  }, []);

  return (
    <div className="p-8 space-y-8">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-extrabold text-[#013362] flex items-center gap-2">
          <Briefcase className="h-6 w-6 text-[#005193]" /> Recruitment
        </h1>
        <div className="flex gap-3">
          <button className="flex items-center gap-2 bg-[#005193] text-white px-4 py-2 rounded-lg text-sm font-semibold hover:opacity-90 transition">
            <Plus className="h-4 w-4" /> Post New Job
          </button>
        </div>
      </div>

      {/* Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: "Total Employees", value: 120, icon: Users },
          { label: "Remote Workers", value: 45, icon: User },
          { label: "On-site Workers", value: 75, icon: Briefcase },
          { label: "Avg Performance", value: "87%", icon: BarChart2 },
        ].map((metric, i) => (
          <div
            key={i}
            className="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm text-center hover:shadow-md transition"
          >
            <metric.icon className="h-6 w-6 mb-1 text-[#005193] mx-auto" />
            <h3 className="text-xl font-bold text-[#013362]">{metric.value}</h3>
            <p className="text-gray-500 text-sm">{metric.label}</p>
          </div>
        ))}
      </div>

      {/* Active Job Postings + AI Insights */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Active Job Postings */}
        <div className="lg:col-span-2 bg-white border border-gray-200 rounded-2xl shadow-sm p-6">
          <h2 className="text-lg font-bold text-[#013362] mb-4 flex items-center gap-2">
            <Briefcase className="h-5 w-5 text-[#005193]" /> Active Job Postings
          </h2>

          <div className="space-y-4">
            {jobs.map((job) => (
              <div
                key={job.id}
                className="border border-gray-200 rounded-xl p-4 flex justify-between items-center hover:bg-[#F8FAFF] transition"
              >
                <div className="flex items-center gap-3">
                  <job.icon className="h-6 w-6 text-[#005193]" />
                  <div>
                    <h3 className="font-semibold text-gray-800">{job.title}</h3>
                    <div className="text-xs text-gray-500 flex gap-4 mt-1">
                      <span>{job.applications} applications</span>
                      <span>{job.qualified} qualified</span>
                    </div>
                  </div>
                </div>
                <button className="text-sm border border-gray-300 text-[#005193] px-4 py-1.5 rounded-lg font-semibold hover:bg-gray-50">
                  View
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* AI Insights */}
        <div className="lg:col-span-1 bg-white border border-gray-200 rounded-2xl shadow-sm p-6 space-y-6">
          <h2 className="text-lg font-bold text-[#013362] mb-4 flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-[#005193]" /> AI Insights
          </h2>
          <div className="bg-white border border-gray-200 rounded-2xl shadow-sm p-6">
            <h3 className="text-md font-bold text-[#013362] flex items-center gap-2 mb-3">
              <Lightbulb className="h-5 w-5 text-[#005193]" /> Top Skill Demand
            </h3>
            <p className="text-sm text-gray-600">
              React and Node.js skills are in high demand this quarter.
            </p>
          </div>

          <div className="bg-white border border-gray-200 rounded-2xl shadow-sm p-6">
            <h3 className="text-md font-bold text-[#013362] flex items-center gap-2 mb-3">
              <TrendingUp className="h-5 w-5 text-[#005193]" /> Hiring Trend
            </h3>
            <p className="text-sm text-gray-600">
              Remote positions receive 40% more applications.
            </p>
          </div>
        </div>
      </div>

      {/* Recent Candidates + Hiring Pipeline */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Candidates */}
        <div className="lg:col-span-2 bg-white border border-gray-200 rounded-2xl shadow-sm p-6">
          <h2 className="text-lg font-bold text-[#013362] mb-4 flex items-center gap-2">
            <Users className="h-5 w-5 text-[#005193]" /> Recent Candidates
          </h2>
          <div className="space-y-3">
            {candidates.map((cand) => (
              <div
                key={cand.id}
                className="flex justify-between items-center border border-gray-200 rounded-xl p-4 hover:bg-[#F8FAFF] transition"
              >
                <div className="flex items-center gap-3">
                  <User className="h-5 w-5 text-[#005193]" />
                  <div>
                    <h4 className="font-semibold text-gray-800">{cand.name}</h4>
                    <p className="text-xs text-gray-500">{cand.role}</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <span className="text-sm font-semibold text-[#005193]">{cand.match} match</span>
                  <button className="border border-gray-300 text-[#005193] px-4 py-1.5 rounded-lg text-xs font-semibold hover:bg-gray-50">
                    Review
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Hiring Pipeline + Quick Actions */}
        <div className="space-y-6">
          <div className="bg-white border border-gray-200 rounded-2xl shadow-sm p-6">
            <h3 className="text-md font-bold text-[#013362] mb-3">Hiring Pipeline</h3>
            <div className="space-y-2 text-sm text-gray-700">
              <div className="bg-[#E8F1FF] px-3 py-2 rounded-lg font-medium">Applied</div>
              <div className="bg-[#D9E8FF] px-3 py-2 rounded-lg font-medium">Screening</div>
              <div className="bg-[#C3DAFF] px-3 py-2 rounded-lg font-medium">Interview</div>
            </div>
          </div>

          <div className="bg-white border border-gray-200 rounded-2xl shadow-sm p-6">
            <h3 className="text-md font-bold text-[#013362] mb-3">Quick Actions</h3>
            <button className="flex items-center gap-2 border border-gray-300 text-[#005193] px-4 py-2 rounded-lg text-sm font-semibold hover:bg-gray-50 w-full justify-center">
              <Mail className="h-4 w-4" /> Send Bulk Messages
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RecruitmentTab;
