import { useCallback, useEffect, useMemo, useState } from 'react'
import './App.css'

const API_BASE = 'http://127.0.0.1:8000'
const TOKEN_KEY = 'skillmatch_access_token'

async function readResponse(response) {
  const data = await response.json().catch(() => ({}))
  if (!response.ok) {
    const detail = typeof data.detail === 'string' ? data.detail : 'Something went wrong. Please try again.'
    throw new Error(detail)
  }
  return data
}

function App() {
  const [jobs, setJobs] = useState([])
  const [allSkills, setAllSkills] = useState([])
  const [search, setSearch] = useState('')
  const [location, setLocation] = useState('')
  const [loadingJobs, setLoadingJobs] = useState(true)
  const [pageError, setPageError] = useState('')

  const [token, setToken] = useState(() => localStorage.getItem(TOKEN_KEY) || '')
  const [profile, setProfile] = useState(null)
  const [mySkills, setMySkills] = useState([])
  const [educations, setEducations] = useState([])
  const [experiences, setExperiences] = useState([])
  const [educationForm, setEducationForm] = useState({ degree: '', field_of_study: '', institution: '', start_date: '', end_date: '' })
  const [experienceForm, setExperienceForm] = useState({ job_title: '', company: '', description: '', start_date: '', end_date: '' })
  const [editingEducationId, setEditingEducationId] = useState(null)
  const [editingExperienceId, setEditingExperienceId] = useState(null)
  const [savingEducation, setSavingEducation] = useState(false)
  const [savingExperience, setSavingExperience] = useState(false)
  const [authMode, setAuthMode] = useState('login')
  const [showAuth, setShowAuth] = useState(false)
  const [showProfile, setShowProfile] = useState(false)
  const [authLoading, setAuthLoading] = useState(false)
  const [profileLoading, setProfileLoading] = useState(false)
  const [authError, setAuthError] = useState('')
  const [profileError, setProfileError] = useState('')
  const [notice, setNotice] = useState('')
  const [authForm, setAuthForm] = useState({ email: '', password: '', first_name: '', last_name: '' })
  const [skillForm, setSkillForm] = useState({ skill_id: '', skill_level: 'Beginner' })
  const [savingSkill, setSavingSkill] = useState(false)

  const [selectedJob, setSelectedJob] = useState(null)
  const [jobDetails, setJobDetails] = useState(null)
  const [jobMatch, setJobMatch] = useState(null)
  const [detailsLoading, setDetailsLoading] = useState(false)
  const [detailsError, setDetailsError] = useState('')

  const apiFetch = useCallback((path, options = {}, authToken = token) => {
    const headers = new Headers(options.headers || {})
    if (options.body && !(options.body instanceof FormData) && !headers.has('Content-Type')) {
      headers.set('Content-Type', 'application/json')
    }
    if (authToken) headers.set('Authorization', `Bearer ${authToken}`)
    return fetch(`${API_BASE}${path}`, { ...options, headers })
  }, [token])

  const loadJobs = useCallback(async () => {
    try {
      setLoadingJobs(true)
      setPageError('')
      const [jobsResponse, skillsResponse] = await Promise.all([
        fetch(`${API_BASE}/api/jobs/`),
        fetch(`${API_BASE}/api/skills/`),
      ])
      const [jobsData, skillsData] = await Promise.all([
        readResponse(jobsResponse),
        readResponse(skillsResponse),
      ])
      setJobs(jobsData)
      setAllSkills(skillsData)
    } catch (error) {
      setPageError(error.message || 'Could not connect to the backend.')
    } finally {
      setLoadingJobs(false)
    }
  }, [])

  const loadProfile = useCallback(async (activeToken = token) => {
    if (!activeToken) return
    try {
      setProfileLoading(true)
      setProfileError('')
      const [profileResponse, skillsResponse, educationResponse, experienceResponse] = await Promise.all([
        apiFetch('/api/users/me', {}, activeToken),
        apiFetch('/api/users/me/skills', {}, activeToken),
        apiFetch('/api/users/me/education', {}, activeToken),
        apiFetch('/api/users/me/experience', {}, activeToken),
      ])
      const [profileData, skillsData, educationData, experienceData] = await Promise.all([
        readResponse(profileResponse),
        readResponse(skillsResponse),
        readResponse(educationResponse),
        readResponse(experienceResponse),
      ])
      setProfile(profileData)
      setMySkills(skillsData)
      setEducations(educationData)
      setExperiences(experienceData)
    } catch (error) {
      setProfileError(error.message || 'Could not load your profile.')
      if (error.message === 'Could not validate credentials' || error.message === 'User not found' || error.message === 'Invalid or expired token' || error.message === 'Not authenticated') {
        localStorage.removeItem(TOKEN_KEY)
        setToken('')
        setProfile(null)
        setMySkills([])
        setEducations([])
        setExperiences([])
      }
    } finally {
      setProfileLoading(false)
    }
  }, [apiFetch, token])

  useEffect(() => {
    loadJobs()
  }, [loadJobs])

  useEffect(() => {
    if (token) loadProfile(token)
    else {
      setProfile(null)
      setMySkills([])
      setEducations([])
      setExperiences([])
    }
  }, [token, loadProfile])
  useEffect(() => {
  if (showAuth) {
    document.getElementById('auth-panel')?.scrollIntoView({
      behavior: 'smooth',
      block: 'center',
    })
  }
}, [showAuth])

  const filteredJobs = useMemo(() => jobs.filter((job) => {
    const query = search.trim().toLowerCase()
    const city = location.trim().toLowerCase()
    const matchesQuery = !query || `${job.title || ''} ${job.company || ''}`.toLowerCase().includes(query)
    const matchesLocation = !city || (job.location || '').toLowerCase().includes(city)
    return matchesQuery && matchesLocation
  }), [jobs, search, location])

  async function openJobDetails(job) {
    setSelectedJob(job)
    setJobDetails(null)
    setJobMatch(null)
    setDetailsError('')
    setDetailsLoading(true)
    try {
      const detailsResponse = await fetch(`${API_BASE}/api/jobs/${job.id}`)
      const detailsData = await readResponse(detailsResponse)
      setJobDetails(detailsData)

      if (token) {
        const matchResponse = await apiFetch(`/api/recommendations/jobs/${job.id}`)
        const matchData = await readResponse(matchResponse)
        setJobMatch(matchData)
      }
    } catch (error) {
      setDetailsError(error.message || 'Could not load job details.')
    } finally {
      setDetailsLoading(false)
    }
  }

  async function submitAuth(event) {
    event.preventDefault()
    setAuthLoading(true)
    setAuthError('')
    setNotice('')
    try {
      if (authMode === 'register') {
        const registerResponse = await fetch(`${API_BASE}/api/auth/register`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(authForm),
        })
        await readResponse(registerResponse)
      }

      const formBody = new URLSearchParams()
      formBody.set('username', authForm.email)
      formBody.set('password', authForm.password)
      const loginResponse = await fetch(`${API_BASE}/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formBody,
      })
      const loginData = await readResponse(loginResponse)
      localStorage.setItem(TOKEN_KEY, loginData.access_token)
      setToken(loginData.access_token)
      setShowAuth(false)
      setShowProfile(true)
      setNotice(authMode === 'register' ? 'Account created successfully.' : 'You are now signed in.')
      setAuthForm({ email: '', password: '', first_name: '', last_name: '' })
    } catch (error) {
      setAuthError(error.message || 'Authentication failed.')
    } finally {
      setAuthLoading(false)
    }
  }

  async function saveSkill(event) {
    event.preventDefault()
    if (!skillForm.skill_id) return
    setSavingSkill(true)
    setProfileError('')
    setNotice('')
    try {
      const response = await apiFetch('/api/users/me/skills', {
        method: 'POST',
        body: JSON.stringify({
          skill_id: Number(skillForm.skill_id),
          skill_level: skillForm.skill_level,
        }),
      })
      await readResponse(response)
      await loadProfile(token)
      setSkillForm({ skill_id: '', skill_level: 'Beginner' })
      setNotice('Skill saved to your profile.')
      setJobMatch(null)
    } catch (error) {
      setProfileError(error.message || 'Could not save this skill.')
    } finally {
      setSavingSkill(false)
    }
  }

  async function removeSkill(skillId) {
    setProfileError('')
    try {
      const response = await apiFetch(`/api/users/me/skills/${skillId}`, { method: 'DELETE' })
      await readResponse(response)
      await loadProfile(token)
      setNotice('Skill removed from your profile.')
      setJobMatch(null)
    } catch (error) {
      setProfileError(error.message || 'Could not remove this skill.')
    }
  }

  async function saveEducation(event) {
    event.preventDefault()
    setSavingEducation(true)
    setProfileError('')
    setNotice('')
    const payload = {
      degree: educationForm.degree.trim(),
      field_of_study: educationForm.field_of_study.trim(),
      institution: educationForm.institution.trim(),
      start_date: educationForm.start_date || null,
      end_date: educationForm.end_date || null,
    }
    try {
      const isEditing = editingEducationId !== null
      const response = await apiFetch(
        isEditing ? `/api/users/me/education/${editingEducationId}` : '/api/users/me/education',
        { method: isEditing ? 'PUT' : 'POST', body: JSON.stringify(payload) },
      )
      await readResponse(response)
      await loadProfile(token)
      setEducationForm({ degree: '', field_of_study: '', institution: '', start_date: '', end_date: '' })
      setEditingEducationId(null)
      setNotice(isEditing ? 'Education updated successfully.' : 'Education added to your profile.')
    } catch (error) {
      setProfileError(error.message || 'Could not save education.')
    } finally {
      setSavingEducation(false)
    }
  }

  function editEducation(item) {
    setEditingEducationId(item.id)
    setEducationForm({
      degree: item.degree || '',
      field_of_study: item.field_of_study || '',
      institution: item.institution || '',
      start_date: item.start_date || '',
      end_date: item.end_date || '',
    })
  }

  async function removeEducation(educationId) {
    setProfileError('')
    try {
      const response = await apiFetch(`/api/users/me/education/${educationId}`, { method: 'DELETE' })
      await readResponse(response)
      await loadProfile(token)
      if (editingEducationId === educationId) {
        setEditingEducationId(null)
        setEducationForm({ degree: '', field_of_study: '', institution: '', start_date: '', end_date: '' })
      }
      setNotice('Education removed from your profile.')
    } catch (error) {
      setProfileError(error.message || 'Could not remove education.')
    }
  }

  async function saveExperience(event) {
    event.preventDefault()
    setSavingExperience(true)
    setProfileError('')
    setNotice('')
    const payload = {
      job_title: experienceForm.job_title.trim(),
      company: experienceForm.company.trim(),
      description: experienceForm.description.trim() || null,
      start_date: experienceForm.start_date,
      end_date: experienceForm.end_date || null,
    }
    try {
      const isEditing = editingExperienceId !== null
      const response = await apiFetch(
        isEditing ? `/api/users/me/experience/${editingExperienceId}` : '/api/users/me/experience',
        { method: isEditing ? 'PUT' : 'POST', body: JSON.stringify(payload) },
      )
      await readResponse(response)
      await loadProfile(token)
      setExperienceForm({ job_title: '', company: '', description: '', start_date: '', end_date: '' })
      setEditingExperienceId(null)
      setNotice(isEditing ? 'Experience updated successfully.' : 'Experience added to your profile.')
    } catch (error) {
      setProfileError(error.message || 'Could not save experience.')
    } finally {
      setSavingExperience(false)
    }
  }

  function editExperience(item) {
    setEditingExperienceId(item.id)
    setExperienceForm({
      job_title: item.job_title || '',
      company: item.company || '',
      description: item.description || '',
      start_date: item.start_date || '',
      end_date: item.end_date || '',
    })
  }

  async function removeExperience(experienceId) {
    setProfileError('')
    try {
      const response = await apiFetch(`/api/users/me/experience/${experienceId}`, { method: 'DELETE' })
      await readResponse(response)
      await loadProfile(token)
      if (editingExperienceId === experienceId) {
        setEditingExperienceId(null)
        setExperienceForm({ job_title: '', company: '', description: '', start_date: '', end_date: '' })
      }
      setNotice('Experience removed from your profile.')
    } catch (error) {
      setProfileError(error.message || 'Could not remove experience.')
    }
  }

  function cancelEducationEdit() {
    setEditingEducationId(null)
    setEducationForm({ degree: '', field_of_study: '', institution: '', start_date: '', end_date: '' })
  }

  function cancelExperienceEdit() {
    setEditingExperienceId(null)
    setExperienceForm({ job_title: '', company: '', description: '', start_date: '', end_date: '' })
  }

  function signOut() {
    localStorage.removeItem(TOKEN_KEY)
    setToken('')
    setProfile(null)
    setMySkills([])
    setEducations([])
    setExperiences([])
    cancelEducationEdit()
    cancelExperienceEdit()
    setShowProfile(false)
    setJobMatch(null)
    setNotice('You have signed out.')
  }

  return (
    <div className="app-shell">
      <header className="navbar">
        <a className="brand" href="#top" aria-label="SkillMatch home">
          <span className="brand-icon">S</span>
          <span>SkillMatch</span>
        </a>
        <nav className="nav-links" aria-label="Main navigation">
          <a href="#jobs">Find jobs</a>
          <a href="#how-it-works">How it works</a>
        </nav>
        <div className="nav-actions">
          {token ? (
            <button className="button button-outline" onClick={() => setShowProfile((value) => !value)}>
              {showProfile ? 'Hide profile' : 'My profile'}
            </button>
          ) : (
            <button className="button button-dark" onClick={() => { setShowAuth(true); setAuthMode('login') }}>
              Sign in
            </button>
          )}
        </div>
      </header>

      <main id="top">
        <section className="hero">
          <div className="hero-copy">
            <span className="eyebrow"><span className="eyebrow-dot" /> CAREER DISCOVERY, REIMAGINED</span>
            <h1>Find work that<br /><span>fits who you are.</span></h1>
            <p>Discover opportunities that match your skills, understand what employers need, and build a clear path toward your next role.</p>
            <div className="hero-actions">
              <a className="button button-primary" href="#jobs">Explore opportunities <span aria-hidden="true">↗</span></a>
              <span className="hero-note"><span className="tiny-check">✓</span> Skill-based recommendations</span>
            </div>
            <div className="hero-stats">
              <div><strong>{jobs.length}</strong><span>opportunities listed</span></div>
              <div><strong>{allSkills.length}</strong><span>skills in the catalogue</span></div>
              <div><strong>AI-ready</strong><span>career insights</span></div>
            </div>
          </div>
          <div className="hero-art" aria-label="Illustration of a job match score">
            <div className="art-orbit orbit-one" />
            <div className="art-orbit orbit-two" />
            <div className="art-spark spark-one">✦</div>
            <div className="art-spark spark-two">✳</div>
            <div className="match-preview">
              <div className="preview-top"><span className="preview-symbol">✦</span><span>YOUR CAREER SNAPSHOT</span><span className="preview-live">LIVE</span></div>
              <div className="preview-score-row"><div><small>SKILL MATCH</small><strong>{jobMatch ? `${Math.round(jobMatch.match_score)}%` : '—'}</strong></div><div className="score-ring"><span>{jobMatch ? `${Math.round(jobMatch.match_score)}%` : '★'}</span></div></div>
              <div className="preview-line"><span /><span /></div>
              <p>{jobMatch ? 'Match calculated from your profile' : 'Your next opportunity starts here'}</p>
            </div>
            <div className="floating-note"><span className="floating-icon">✓</span><div><strong>Skills first</strong><small>Find your next step</small></div></div>
          </div>
        </section>

        {notice && <div className="notice-banner" role="status"><span>✓</span>{notice}<button aria-label="Dismiss message" onClick={() => setNotice('')}>×</button></div>}
        {pageError && <div className="error-banner" role="alert"><strong>Backend connection issue</strong><span>{pageError}</span><button className="button button-outline" onClick={loadJobs}>Retry</button></div>}

        {showAuth && (
          <section id="auth-panel" className="panel auth-panel" aria-labelledby="auth-heading">
            <div className="panel-heading"><div><span className="eyebrow">YOUR SKILLMATCH ACCOUNT</span><h2 id="auth-heading">{authMode === 'login' ? 'Welcome back' : 'Create your account'}</h2><p>Sign in to save your skills and see personalized job matches.</p></div><button className="icon-button" onClick={() => setShowAuth(false)} aria-label="Close sign in">×</button></div>
            <div className="auth-tabs"><button className={authMode === 'login' ? 'selected' : ''} onClick={() => { setAuthMode('login'); setAuthError('') }}>Sign in</button><button className={authMode === 'register' ? 'selected' : ''} onClick={() => { setAuthMode('register'); setAuthError('') }}>Create account</button></div>
            <form className="form-grid" onSubmit={submitAuth}>
              {authMode === 'register' && <>
                <label>First name<input required value={authForm.first_name} onChange={(event) => setAuthForm({ ...authForm, first_name: event.target.value })} autoComplete="given-name" /></label>
                <label>Last name<input required value={authForm.last_name} onChange={(event) => setAuthForm({ ...authForm, last_name: event.target.value })} autoComplete="family-name" /></label>
              </>}
              <label className="full-field">Email address<input type="email" required value={authForm.email} onChange={(event) => setAuthForm({ ...authForm, email: event.target.value })} autoComplete="email" /></label>
              <label className="full-field">Password<input type="password" required minLength={8} value={authForm.password} onChange={(event) => setAuthForm({ ...authForm, password: event.target.value })} autoComplete={authMode === 'login' ? 'current-password' : 'new-password'} /></label>
              {authError && <p className="form-error full-field" role="alert">{authError}</p>}
              <button className="button button-primary full-field" type="submit" disabled={authLoading}>{authLoading ? 'Please wait…' : authMode === 'login' ? 'Sign in to SkillMatch' : 'Create account and sign in'}</button>
            </form>
          </section>
        )}

        {showProfile && token && (
          <section className="panel profile-panel" id="profile" aria-labelledby="profile-heading">
            <div className="panel-heading"><div><span className="eyebrow">PERSONAL WORKSPACE</span><h2 id="profile-heading">{profile ? `Welcome, ${profile.first_name}` : 'Your profile'}</h2><p>Keep your skill profile current to get more useful matches.</p></div><button className="button button-outline" onClick={signOut}>Sign out</button></div>
            {profileLoading ? <p className="muted">Loading profile…</p> : <>
              {profile && <p className="profile-email">{profile.email}</p>}
              {profileError && <p className="form-error" role="alert">{profileError}</p>}
              <form className="skill-form" onSubmit={saveSkill}>
                <label>Skill<select required value={skillForm.skill_id} onChange={(event) => setSkillForm({ ...skillForm, skill_id: event.target.value })}><option value="">Choose a skill</option>{allSkills.map((skill) => <option key={skill.id} value={skill.id}>{skill.name}</option>)}</select></label>
                <label>Proficiency<select value={skillForm.skill_level} onChange={(event) => setSkillForm({ ...skillForm, skill_level: event.target.value })}><option>Beginner</option><option>Intermediate</option><option>Advanced</option></select></label>
                <button className="button button-primary" type="submit" disabled={savingSkill}>{savingSkill ? 'Saving…' : 'Add / update skill'}</button>
              </form>
              <div className="profile-skills-heading"><h3>Your skills</h3><span>{mySkills.length} added</span></div>
              {mySkills.length ? <div className="profile-skills">{mySkills.map((skill) => <div className="profile-skill" key={skill.id}><div><strong>{skill.name}</strong><span>{skill.skill_level}</span></div><button onClick={() => removeSkill(skill.id)} aria-label={`Remove ${skill.name}`} title="Remove skill">×</button></div>)}</div> : <div className="empty-inline">No skills added yet. Add your first skill above to personalize recommendations.</div>}

              <div className="profile-skills-heading"><h3>Education</h3><span>{educations.length} added</span></div>
              <form className="form-grid profile-record-form" onSubmit={saveEducation}>
                <label>Degree<input required value={educationForm.degree} onChange={(event) => setEducationForm({ ...educationForm, degree: event.target.value })} placeholder="e.g. Bachelor's degree" /></label>
                <label>Field of study<input required value={educationForm.field_of_study} onChange={(event) => setEducationForm({ ...educationForm, field_of_study: event.target.value })} placeholder="e.g. Computer Science" /></label>
                <label className="full-field">Institution<input required value={educationForm.institution} onChange={(event) => setEducationForm({ ...educationForm, institution: event.target.value })} placeholder="University or institution" /></label>
                <label>Start date<input type="date" required value={educationForm.start_date} onChange={(event) => setEducationForm({ ...educationForm, start_date: event.target.value })} /></label>
                <label>End date (optional)<input type="date" value={educationForm.end_date} onChange={(event) => setEducationForm({ ...educationForm, end_date: event.target.value })} /></label>
                <div className="full-field profile-form-actions"><button className="button button-primary" type="submit" disabled={savingEducation}>{savingEducation ? 'Saving…' : editingEducationId ? 'Update education' : 'Add education'}</button>{editingEducationId && <button className="button button-outline" type="button" onClick={cancelEducationEdit}>Cancel edit</button>}</div>
              </form>
              {educations.length ? <div className="profile-record-list">{educations.map((item) => <article className="profile-record" key={item.id}><div><strong>{item.degree} — {item.field_of_study}</strong><p>{item.institution}</p><span>{item.start_date || 'Start date not specified'} – {item.end_date || 'Present'}</span></div><div className="profile-record-actions"><button className="button button-outline" type="button" onClick={() => editEducation(item)}>Edit</button><button className="button button-outline" type="button" onClick={() => removeEducation(item.id)}>Delete</button></div></article>)}</div> : <div className="empty-inline">No education added yet.</div>}

              <div className="profile-skills-heading"><h3>Work experience</h3><span>{experiences.length} added</span></div>
              <form className="form-grid profile-record-form" onSubmit={saveExperience}>
                <label>Job title<input required value={experienceForm.job_title} onChange={(event) => setExperienceForm({ ...experienceForm, job_title: event.target.value })} placeholder="e.g. Software Developer Intern" /></label>
                <label>Company<input required value={experienceForm.company} onChange={(event) => setExperienceForm({ ...experienceForm, company: event.target.value })} placeholder="Company name" /></label>
                <label className="full-field">Description (optional)<textarea value={experienceForm.description} onChange={(event) => setExperienceForm({ ...experienceForm, description: event.target.value })} placeholder="Your responsibilities and achievements" rows={3} /></label>
                <label>Start date<input type="date" required value={experienceForm.start_date} onChange={(event) => setExperienceForm({ ...experienceForm, start_date: event.target.value })} /></label>
                <label>End date (optional)<input type="date" value={experienceForm.end_date} onChange={(event) => setExperienceForm({ ...experienceForm, end_date: event.target.value })} /></label>
                <div className="full-field profile-form-actions"><button className="button button-primary" type="submit" disabled={savingExperience}>{savingExperience ? 'Saving…' : editingExperienceId ? 'Update experience' : 'Add experience'}</button>{editingExperienceId && <button className="button button-outline" type="button" onClick={cancelExperienceEdit}>Cancel edit</button>}</div>
              </form>
              {experiences.length ? <div className="profile-record-list">{experiences.map((item) => <article className="profile-record" key={item.id}><div><strong>{item.job_title} — {item.company}</strong>{item.description && <p>{item.description}</p>}<span>{item.start_date} – {item.end_date || 'Present'}</span></div><div className="profile-record-actions"><button className="button button-outline" type="button" onClick={() => editExperience(item)}>Edit</button><button className="button button-outline" type="button" onClick={() => removeExperience(item.id)}>Delete</button></div></article>)}</div> : <div className="empty-inline">No work experience added yet.</div>}
            </>}
          </section>
        )}

        <section className="jobs-section" id="jobs">
          <div className="section-heading"><div><span className="eyebrow">THE NEXT STEP STARTS HERE</span><h2>Explore opportunities</h2><p>Search real jobs and open a role to inspect its skill requirements.</p></div><span className="job-count"><span className="count-dot" />{loadingJobs ? 'Loading jobs…' : `${filteredJobs.length} ${filteredJobs.length === 1 ? 'job' : 'jobs'} found`}</span></div>
          <div className="search-panel">
            <label><span>Job title or company</span><div className="input-with-icon"><span aria-hidden="true">⌕</span><input type="search" placeholder="Try Python Developer" value={search} onChange={(event) => setSearch(event.target.value)} /></div></label>
            <label><span>Location</span><div className="input-with-icon"><span aria-hidden="true">⌖</span><input type="search" placeholder="City or region" value={location} onChange={(event) => setLocation(event.target.value)} /></div></label>
            <button className="button button-dark search-button" onClick={() => { setSearch(search.trim()); setLocation(location.trim()) }}>Search jobs <span aria-hidden="true">→</span></button>
          </div>

          <div className="jobs-list">
            {loadingJobs ? <div className="loading-card"><span className="spinner" />Loading opportunities from the database…</div> : filteredJobs.length ? filteredJobs.map((job) => {
              const match = job.id === selectedJob?.id ? jobMatch : null
              return <article className={`job-card ${selectedJob?.id === job.id ? 'job-card-active' : ''}`} key={job.id}>
                <div className="company-icon">{(job.company || '?').charAt(0).toUpperCase()}</div>
                <div className="job-info"><h3>{job.title}</h3><p className="company-name">{job.company}</p><div className="job-meta"><span>⌖ {job.location || 'Location flexible'}</span><span>◷ {job.employment_type || 'Employment type not specified'}</span></div></div>
                <div className="job-card-side">{token && match ? <div className="match-score"><strong>{Math.round(match.match_score)}%</strong><span>skill match</span></div> : <span className="job-tag">Career opportunity</span>}<button className="details-link" onClick={() => openJobDetails(job)}>{selectedJob?.id === job.id ? 'Refresh details' : 'View details'} <span aria-hidden="true">↗</span></button></div>
              </article>
            }) : <div className="empty-state"><span className="empty-icon">⌕</span><h3>No jobs found</h3><p>Try a different job title or location.</p><button className="button button-outline" onClick={() => { setSearch(''); setLocation('') }}>Clear search</button></div>}
          </div>
        </section>

        {(selectedJob || detailsLoading || detailsError) && <section className="job-details panel" id="job-details" aria-live="polite">
          <div className="panel-heading"><div><span className="eyebrow">ROLE BREAKDOWN</span><h2>{jobDetails?.title || selectedJob?.title || 'Job details'}</h2><p>{jobDetails ? `${jobDetails.company} · ${jobDetails.location || 'Location not specified'} · ${jobDetails.employment_type || 'Type not specified'}` : 'Loading role information…'}</p></div><button className="icon-button" onClick={() => { setSelectedJob(null); setJobDetails(null); setJobMatch(null); setDetailsError('') }} aria-label="Close job details">×</button></div>
          {detailsLoading && <div className="loading-card"><span className="spinner" />Loading job details and match analysis…</div>}
          {detailsError && <p className="form-error" role="alert">{detailsError}{!token && ' Sign in to see your personalized match score.'}</p>}
          {jobDetails && !detailsLoading && <>
            <p className="job-description">{jobDetails.description || 'No description was provided for this role.'}</p>
            <div className="detail-summary"><div><span>Company</span><strong>{jobDetails.company}</strong></div><div><span>Location</span><strong>{jobDetails.location || 'Not specified'}</strong></div><div><span>Employment</span><strong>{jobDetails.employment_type || 'Not specified'}</strong></div></div>
            {jobMatch ? <>
              <div className="match-result"><div className="match-result-score"><span>YOUR MATCH SCORE</span><strong>{Math.round(jobMatch.match_score)}<small>%</small></strong><div className="score-track"><span style={{ width: `${Math.max(0, Math.min(100, jobMatch.match_score))}%` }} /></div></div><div className="match-result-copy"><h3>{jobMatch.match_score >= 80 ? 'Strong match' : jobMatch.match_score >= 50 ? 'A promising start' : 'A chance to grow'}</h3><p>Your score is calculated from the skills and proficiency levels saved in your profile, with greater weight given to required skills.</p><div className="match-pills"><span className="pill-success">✓ {jobMatch.matched_skills?.length || 0} matched</span><span className="pill-warning">＋ {(jobMatch.missing_required_skills?.length || 0) + (jobMatch.missing_optional_skills?.length || 0)} to develop</span></div></div></div>
              <h3 className="subsection-title">Skill-by-skill analysis</h3>
              <div className="skill-analysis">{(jobMatch.skill_details || []).map((skill) => <div className="analysis-row" key={skill.skill_id}><div className={`skill-status ${skill.is_present ? 'status-present' : 'status-missing'}`}>{skill.is_present ? '✓' : '＋'}</div><div className="analysis-main"><strong>{skill.skill_name}</strong><span>{skill.is_required ? 'Required skill' : 'Optional skill'} · Target: {skill.required_level || 'Any level'}</span></div><div className="analysis-level"><span>{skill.user_level || 'Not added'}</span>{skill.user_level && <small>your level</small>}</div></div>)}</div>
              {jobMatch.learning_recommendations?.length > 0 && <><h3 className="subsection-title">Recommended next steps</h3><div className="learning-list">{jobMatch.learning_recommendations.map((item) => <article className="learning-card" key={item.skill_id}><span className={`priority-dot ${item.priority === 'high' ? 'priority-high' : ''}`} /><div><div className="learning-title"><strong>{item.skill_name}</strong><span>{item.priority === 'high' ? 'High priority' : 'Optional skill'}</span></div><p>{item.message}</p></div></article>)}</div></>}
            </> : <div className="sign-in-callout"><div><strong>See your personal match score</strong><p>Sign in and add your skills to compare your profile with this job.</p></div><button className="button button-primary" onClick={() => { setShowAuth(true); setAuthMode('login') }}>Sign in</button></div>}
          </>}
        </section>}

        <section className="how-section" id="how-it-works"><div className="how-heading"><span className="eyebrow">A CLEARER WAY FORWARD</span><h2>From skills to your next opportunity</h2><p>Three simple steps turn your profile into a practical career plan.</p></div><div className="steps"><article><span className="step-number">01</span><div className="step-icon">◎</div><h3>Build your profile</h3><p>Add the skills you already have and set your proficiency level.</p></article><article><span className="step-number">02</span><div className="step-icon">✳</div><h3>Explore your matches</h3><p>Compare your skills against real job requirements and match scores.</p></article><article><span className="step-number">03</span><div className="step-icon">↗</div><h3>Close the skill gap</h3><p>See which required skills to develop next and where to focus.</p></article></div></section>
      </main>

      <footer className="footer"><a className="brand" href="#top"><span className="brand-icon">S</span><span>SkillMatch</span></a><p>Intelligent Job and Skill Recommendation System</p><span>Built around skills. Designed for growth.</span></footer>
    </div>
  )
}

export default App
