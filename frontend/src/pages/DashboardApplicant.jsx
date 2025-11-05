import React from 'react';
import TopNavbarApplicant from "../components/TopNavbarApplicant";
import { Briefcase, Send, Eye, Users, Sparkles, FileText, User, BarChart2, Download, Mail, Calendar, UserCheck } from "lucide-react";

export default function DashboardApplicant() {
  const [activeTab, setActiveTab] = React.useState("dashboard");
  const [username, setUsername] = React.useState("");

  React.useEffect(() => {
    async function fetchUsername() {
      const token = localStorage.getItem('token');
      if (!token) return;
      try {
        const res = await fetch('/api/auth/me', {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });
        if (res.ok) {
          const data = await res.json();
          // Prefer first_name + last_name, fallback to username/email
          if (data.first_name || data.last_name) {
            setUsername(`${data.first_name || ''} ${data.last_name || ''}`.trim());
          } else {
            setUsername(data.username || data.email || "User");
          }
        }
      } catch (err) {
        setUsername("User");
      }
    }
    fetchUsername();
  }, []);

  const stats = [
    { label: "Applications Sent", value: 24, sub: "+12% from last month", icon: Send },
    { label: "Profile Views", value: 8, sub: "+3 new views", icon: Eye },
    { label: "Interview Requests", value: 5, sub: "2 new today", icon: Briefcase },
    { label: "AI Job Match", value: "92%", sub: "excellent match", icon: Sparkles },
  ];

  const recommendedJobs = [
    {
      company: "Abibas",
      title: "Senior Frontend Developer",
      tags: ["React", "TypeScript", "Node.js"],
    },
    {
      company: "Naike",
      title: "Full Stack Engineer",
      tags: ["Python", "Postgres", "Django"],
    },
  ];

  const recentActivity = [
    { icon: Mail, color: "#005193", text: "Applied to XYZ Company", time: "2 weeks ago" },
    { icon: Eye, color: "#005193", text: "Profile viewed by ABC recruiter", time: "3 weeks ago" },
    { icon: Calendar, color: "#005193", text: "Interview scheduled with ABC", time: "1 month ago" },
    { icon: UserCheck, color: "#005193", text: "Updated profile details", time: "1 month ago" },
  ];

  const upcomingInterviews = [
    { company: "ABC Company", role: "Senior Developer" },
    { company: "XYZ Company", role: "Frontend Developer" },
  ];

  return (
    <section className="min-h-screen flex flex-col bg-gradient-to-br from-[#F7F8FF] via-[#e3e9ff] to-[#dbeafe] font-inter">
      <TopNavbarApplicant activeTab={activeTab} setActiveTab={setActiveTab} />
      <main className="flex-1 p-8 flex flex-col gap-6">
        {activeTab === "dashboard" && (
          <>
            <div className="flex items-center mb-2">
              <h1 className="text-2xl font-extrabold text-[#013362]">
                  Welcome, <span className="font-semibold">{username || "User"}</span>
              </h1>
            </div>
            {/* Stats Section */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              {stats.map((stat, i) => (
                <div
                  key={i}
                  className="bg-white rounded-2xl p-6 border border-gray-200 shadow-sm text-center hover:shadow-md transition flex flex-col items-center"
                >
                  {stat.icon && <stat.icon className="h-7 w-7 mb-2 text-[#005193]" />}
                  <h3 className="text-3xl font-extrabold text-[#013362]">{stat.value}</h3>
                  <p className="text-gray-500 mt-1 text-sm font-medium">{stat.label}</p>
                  <p className="text-xs text-green-600 mt-1">{stat.sub}</p>
                </div>
              ))}
            </div>
            {/* Main Content */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* AI Recommended Jobs */}
              <div className="md:col-span-2 bg-white rounded-2xl border border-gray-200 p-6 shadow-sm">
                <div className="flex justify-between items-center mb-4">
                  <h2 className="text-lg font-bold text-[#013362] flex items-center gap-2">
                    <FileText className="h-5 w-5 text-[#005193]" /> AI Recommended Jobs
                  </h2>
                  <button className="text-[#005193] text-sm font-semibold hover:underline flex items-center gap-1">
                    <BarChart2 className="h-4 w-4" /> View All
                  </button>
                </div>
                <div className="space-y-4">
                  {recommendedJobs.map((job, i) => (
                    <div
                      key={i}
                      className="flex justify-between items-start border border-gray-200 rounded-lg px-4 py-3 hover:bg-[#F7F8FF] transition"
                    >
                      <div>
                        <div className="flex items-center space-x-2">
                          <div className="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center text-sm font-bold uppercase text-gray-600">
                            {job.company[0]}
                          </div>
                          <div>
                            <p className="font-medium text-gray-800">{job.title}</p>
                            <p className="text-sm text-gray-500">{job.company}</p>
                          </div>
                        </div>
                        <div className="flex flex-wrap gap-2 mt-2">
                          {job.tags.map((tag) => (
                            <span
                              key={tag}
                              className="bg-blue-100 text-[#2563eb] text-xs px-3 py-1 rounded-full border border-blue-200 font-medium"
                              style={{ marginBottom: '2px' }}
                            >
                              {tag}
                            </span>
                          ))}
                        </div>
                      </div>
                      <div className="flex flex-col items-end space-y-2">
                        <button className="px-3 py-1 rounded-md text-sm font-semibold flex items-center gap-2 text-[#005193] hover:underline bg-transparent border-none shadow-none">
                          View Details
                        </button>
                        <button className="px-5 py-2 rounded-md text-sm font-semibold flex items-center gap-2 bg-gradient-to-r from-[#005193] to-[#013362] text-white shadow-lg hover:opacity-90 transition">
                          Apply Now
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
              {/* Recent Activity */}
              <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm">
                <h2 className="text-lg font-bold text-[#013362] mb-4 flex items-center gap-2">
                  <Users className="h-5 w-5 text-[#005193]" /> Recent Activity
                </h2>
                <ul className="space-y-3">
                  {recentActivity.map((item, i) => (
                    <li key={i} className="flex items-start space-x-3">
                      <item.icon className="h-5 w-5 mt-1" style={{ color: item.color }} />
                      <div>
                        <p className="text-sm text-gray-800">{item.text}</p>
                        <p className="text-xs text-gray-500">{item.time}</p>
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
            {/* Upcoming Interviews */}
            <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm">
              <h2 className="text-lg font-bold text-[#013362] mb-4 flex items-center gap-2">
                <Briefcase className="h-5 w-5 text-[#005193]" /> Upcoming Interviews
              </h2>
              <div className="grid md:grid-cols-2 gap-4">
                {upcomingInterviews.map((interview, i) => (
                  <div
                    key={i}
                    className="border rounded-md p-4 flex flex-col md:flex-row justify-between items-start md:items-center hover:bg-[#F7F8FF]"
                  >
                    <div>
                      <p className="font-medium text-gray-800">{interview.company}</p>
                      <p className="text-sm text-gray-500">{interview.role}</p>
                    </div>
                    <div className="flex space-x-2 mt-3 md:mt-0">
                      <button className="px-3 py-1 rounded-md text-sm font-semibold flex items-center gap-2 text-[#005193] hover:underline bg-transparent border-none shadow-none">
                        View Details
                      </button>
                      <button className="px-5 py-2 rounded-md text-sm font-semibold flex items-center gap-2 bg-gradient-to-r from-[#005193] to-[#013362] text-white shadow-lg hover:opacity-90 transition">
                        Join Interview
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </>
        )}
        {/* Placeholder content for other tabs */}
        {activeTab === "jobs" && (
          <div className="flex-1 flex items-center justify-center text-2xl text-gray-400 font-semibold">Jobs tab content coming soon...</div>
        )}
        {activeTab === "applications" && (
          <div className="flex-1 flex items-center justify-center text-2xl text-gray-400 font-semibold">Applications tab content coming soon...</div>
        )}
        {activeTab === "profile" && (
          <div className="flex-1 flex items-center justify-center text-2xl text-gray-400 font-semibold">Profile tab content coming soon...</div>
        )}
        {activeTab === "chat" && (
          <div className="flex-1 flex items-center justify-center text-2xl text-gray-400 font-semibold">Chat tab content coming soon...</div>
        )}
      </main>
    </section>
  );
};

