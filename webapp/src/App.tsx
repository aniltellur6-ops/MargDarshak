import { useState, useEffect } from "react";
import { Loader2, UploadCloud, FileText, CheckCircle2, TrendingUp, AlertTriangle, ArrowRight, Zap, Target, BookOpen } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import type { Variants } from "framer-motion";
import { getLiveNews, analyzeProfile } from "./lib/api";

const containerVariants: Variants = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
};

const itemVariants: Variants = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { type: "spring", stiffness: 300, damping: 24 } }
};

export default function App() {
  const [news, setNews] = useState<any[]>([]);
  const [loadingNews, setLoadingNews] = useState(true);
  
  const [file, setFile] = useState<File | null>(null);
  const [jd, setJd] = useState("");
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState<any>(null);

  useEffect(() => {
    getLiveNews().then((data) => {
      setNews(data);
      setLoadingNews(false);
    }).catch(err => {
      console.error(err);
      setLoadingNews(false);
    });
  }, []);

  const handleAnalyze = async () => {
    if (!file) return alert("Please select a resume file");
    setAnalyzing(true);
    setResult(null);
    try {
      const formData = new FormData();
      formData.append("resume_file", file);
      if (jd) {
        formData.append("job_description", jd);
      }
      const data = await analyzeProfile(formData);
      setResult(data);
    } catch (err) {
      console.error(err);
      alert("Analysis failed.");
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <>
      <div className="animated-bg" />
      <div className="min-h-screen p-4 md:p-8 max-w-[1400px] mx-auto flex flex-col xl:flex-row gap-8 relative z-10">
        
        {/* Main Content */}
        <motion.div 
          variants={containerVariants}
          initial="hidden"
          animate="show"
          className="flex-1 flex flex-col space-y-8"
        >
          <motion.div variants={itemVariants} className="pt-4 pb-2">
            <div className="flex items-center gap-3 mb-4">
              <motion.div 
                whileHover={{ rotate: 15, scale: 1.1 }}
                className="h-12 w-12 rounded-2xl bg-white shadow-xl flex items-center justify-center border border-indigo-100"
              >
                <Zap className="text-brand-500 h-7 w-7" />
              </motion.div>
              <h1 className="text-5xl md:text-6xl font-extrabold tracking-tight text-slate-800 drop-shadow-sm">
                MargDarshak <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-500 to-fuchsia-500">AI</span>
              </h1>
            </div>
            <p className="text-slate-600 text-lg max-w-2xl leading-relaxed font-medium">
              Upload your resume and a target job description. Our AI analyzes your skills, identifies critical gaps, and builds a prioritized learning path.
            </p>
          </motion.div>

          <motion.div variants={itemVariants} className="glass-panel p-6 md:p-8 space-y-6">
            {/* File Upload */}
            <div>
              <h2 className="text-lg font-bold mb-3 flex items-center gap-2 text-slate-700">
                <UploadCloud className="text-brand-500 h-5 w-5" /> 1. Upload Resume (PDF/DOCX)
              </h2>
              <motion.div 
                whileHover={{ scale: 1.01 }}
                whileTap={{ scale: 0.99 }}
                className="relative group cursor-pointer rounded-2xl overflow-hidden"
              >
                <input 
                  type="file" 
                  accept=".pdf,.docx" 
                  onChange={e => setFile(e.target.files?.[0] || null)}
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                />
                <div className="bg-white/40 border-dashed border-2 border-slate-300 p-8 flex flex-col items-center justify-center text-center group-hover:border-brand-400 group-hover:bg-brand-50/50 transition-all rounded-2xl">
                  <FileText className="h-12 w-12 text-slate-400 mb-3 group-hover:text-brand-500 transition-colors" />
                  <span className="text-slate-700 font-semibold text-lg">
                    {file ? file.name : "Drag & drop your resume or click to browse"}
                  </span>
                  {!file && <span className="text-slate-500 text-sm mt-1 font-medium">Supports .pdf and .docx</span>}
                </div>
              </motion.div>
            </div>

            {/* JD */}
            <div>
              <h2 className="text-lg font-bold mb-3 flex items-center gap-2 pt-2 text-slate-700">
                <Target className="text-fuchsia-500 h-5 w-5" /> 2. Target Job Description <span className="text-slate-400 text-sm font-medium">(Optional)</span>
              </h2>
              <textarea 
                value={jd}
                onChange={e => setJd(e.target.value)}
                className="glass-input w-full h-32 resize-none shadow-sm"
                placeholder="Paste the job description you are targeting..."
              />
            </div>

            <motion.button 
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={handleAnalyze} 
              disabled={analyzing || !file}
              className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed mt-4 text-lg py-4"
            >
              {analyzing ? (
                <>
                  <Loader2 className="animate-spin h-6 w-6" />
                  Running Deep Analysis...
                </>
              ) : (
                <>
                  Generate Career Analysis <ArrowRight className="h-6 w-6 ml-2" />
                </>
              )}
            </motion.button>
          </motion.div>

          <AnimatePresence>
            {result && (
              <motion.div 
                initial={{ opacity: 0, scale: 0.95, y: 20 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                transition={{ type: "spring", stiffness: 300, damping: 25 }}
                className="glass-panel p-6 md:p-8 space-y-8 bg-white/80"
              >
                <div className="flex flex-col md:flex-row md:items-center justify-between border-b border-slate-200 pb-6 gap-4">
                  <h2 className="text-3xl font-extrabold text-slate-800">Intelligence Report</h2>
                  {result.match && (
                    <motion.div 
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      transition={{ type: "spring", bounce: 0.5, delay: 0.2 }}
                      className="flex items-center gap-3 bg-emerald-50 px-5 py-3 rounded-xl border border-emerald-100 shadow-sm"
                    >
                      <span className="text-emerald-700 text-sm font-bold uppercase tracking-wider">Match Score</span>
                      <span className="text-3xl font-black text-emerald-600">
                        {Math.round(result.match.match_score * 100)}%
                      </span>
                    </motion.div>
                  )}
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* Profile Overview */}
                  <motion.div 
                    whileHover={{ y: -5 }}
                    className="bg-slate-50/80 p-6 rounded-2xl border border-slate-200 shadow-sm"
                  >
                    <h3 className="font-bold flex items-center gap-2 text-slate-800 mb-5 text-lg">
                      <CheckCircle2 className="text-brand-500 h-6 w-6" /> Profile Overview
                    </h3>
                    <div className="space-y-3 mb-5 text-sm">
                      <p className="flex justify-between border-b border-slate-100 pb-2"><span className="text-slate-500 font-medium">Education:</span> <span className="text-slate-800 font-semibold text-right">{result.profile.education_degree || "N/A"}</span></p>
                      <p className="flex justify-between border-b border-slate-100 pb-2"><span className="text-slate-500 font-medium">Target Role:</span> <span className="text-slate-800 font-semibold text-right">{result.profile.target_role || "N/A"}</span></p>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {result.profile.evidences.map((e: any, i: number) => (
                        <span key={i} className="px-3 py-1.5 bg-white text-slate-600 border border-slate-200 shadow-sm font-medium text-xs rounded-lg">
                          {e.skill_name}
                        </span>
                      ))}
                    </div>
                  </motion.div>

                  {/* Missing Skills */}
                  {result.job && result.match && (
                    <motion.div 
                      whileHover={{ y: -5 }}
                      className="bg-rose-50/80 p-6 rounded-2xl border border-rose-100 shadow-sm"
                    >
                      <h3 className="font-bold flex items-center gap-2 text-rose-700 mb-5 text-lg">
                        <AlertTriangle className="h-6 w-6" /> Missing Skills
                      </h3>
                      <div className="flex flex-wrap gap-2">
                        {result.gap.missing_mandatory_skills?.length > 0 ? (
                          result.gap.missing_mandatory_skills.map((s: string, i: number) => (
                            <span key={i} className="px-3 py-1.5 bg-white text-rose-600 border border-rose-200 shadow-sm font-medium text-xs rounded-lg">
                              {s}
                            </span>
                          ))
                        ) : (
                          <span className="text-slate-500 font-medium">No mandatory skills missing!</span>
                        )}
                      </div>
                    </motion.div>
                  )}
                </div>

                {/* Priority Learning */}
                {result.job && result.priority && (
                  <div className="pt-4">
                    <h3 className="font-bold flex items-center gap-2 text-fuchsia-600 mb-6 text-xl">
                      <BookOpen className="h-6 w-6" /> Prioritized Learning Path
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {result.priority.prioritized_gaps.map((p: any, i: number) => (
                        <motion.div 
                          key={i} 
                          whileHover={{ scale: 1.02 }}
                          className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex justify-between items-center group"
                        >
                          <div className="flex items-center gap-4">
                            <div className="h-10 w-10 rounded-xl bg-fuchsia-50 text-fuchsia-600 flex items-center justify-center font-black text-lg border border-fuchsia-100">
                              {i + 1}
                            </div>
                            <span className="font-bold text-slate-700 text-base">{p.skill_id}</span> 
                          </div>
                          <span className="text-xs uppercase font-bold bg-slate-100 text-slate-500 px-3 py-1.5 rounded-lg">
                            Priority {p.priority_score.toFixed(1)}
                          </span>
                        </motion.div>
                      ))}
                    </div>
                  </div>
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>

        {/* Sidebar - News */}
        <motion.div 
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3, type: "spring", stiffness: 200 }}
          className="w-full xl:w-[450px] flex flex-col"
        >
          <div className="glass-panel p-6 flex flex-col h-full max-h-[85vh] sticky top-8 bg-white/60">
            <div className="flex items-center justify-between mb-6 pb-4 border-b border-slate-200">
              <h2 className="text-2xl font-extrabold flex items-center gap-2 text-slate-800">
                <TrendingUp className="text-brand-500 h-7 w-7" /> Market Pulse
              </h2>
              {loadingNews && <Loader2 className="animate-spin h-5 w-5 text-brand-500" />}
            </div>
            
            <div className="flex-1 overflow-y-auto pr-3 space-y-5 custom-scrollbar">
              {news.map((item, idx) => (
                <motion.div 
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: idx * 0.1 }}
                  key={idx} 
                  className="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm hover:shadow-md hover:border-brand-200 transition-all group"
                >
                  <h3 className="font-bold text-slate-800 mb-3 text-sm leading-relaxed group-hover:text-brand-600 transition-colors">
                    {item.title}
                  </h3>
                  
                  <div className="flex items-center justify-between mb-4">
                    <span className={`text-[10px] px-2.5 py-1 rounded-md font-black uppercase tracking-wider shadow-sm ${
                      item.impact_score > 7 ? 'bg-rose-100 text-rose-700 border border-rose-200' :
                      item.impact_score > 4 ? 'bg-amber-100 text-amber-700 border border-amber-200' :
                      'bg-sky-100 text-sky-700 border border-sky-200'
                    }`}>
                      Impact: {item.impact_score}/10
                    </span>
                  </div>
                  
                  {item.impacted_skills?.length > 0 && (
                    <div className="flex flex-wrap gap-1.5 mt-2">
                      {item.impacted_skills.map((s: string, i: number) => (
                        <span key={i} className="text-[10px] bg-slate-50 text-slate-600 px-2 py-1 rounded-lg border border-slate-200 font-medium">
                          {s}
                        </span>
                      ))}
                    </div>
                  )}
                </motion.div>
              ))}
              
              {!loadingNews && news.length === 0 && (
                <div className="text-center py-16 flex flex-col items-center justify-center opacity-70">
                  <AlertTriangle className="h-10 w-10 text-slate-400 mb-4" />
                  <p className="text-slate-500 font-medium">No market updates currently available.</p>
                </div>
              )}
            </div>
          </div>
        </motion.div>
      </div>
    </>
  );
}
