const API_BASE = '/api';
let authToken = localStorage.getItem('access_token');

function showError(id, msg) {
	const el = document.getElementById(id);
	if (!el) return;
	el.innerText = msg;
	el.style.display = 'block';
	setTimeout(() => { if (el) el.style.display = 'none' }, 4000);
}

async function apiRequest(endpoint, method = 'GET', body) {
	const headers = { 'Content-Type': 'application/json' };
	if (authToken) headers['Authorization'] = 'Bearer ' + authToken;
	const res = await fetch(API_BASE + endpoint, { method, headers, body: body ? JSON.stringify(body) : undefined });
	if (res.status === 401 && authToken) { localStorage.removeItem('access_token'); authToken = null; window.location.reload(); }
	return res;
}

function showAuth(sl) {
	document.getElementById('loginForm').style.display = sl ? 'block' : 'none';
	document.getElementById('registerForm').style.display = sl ? 'none' : 'block';
}

function logout() {
	localStorage.removeItem('access_token');
	authToken = null;
	document.getElementById('authSection').style.display = 'block';
	document.getElementById('chatSection').style.display = 'none';
}

function addMessage(text, isUser) {
	const c = document.getElementById('chatMessages');
	const d = document.createElement('div');
	d.className = 'message ' + (isUser ? 'user-message' : 'bot-message');
	d.innerText = text;
	c.appendChild(d);
	c.scrollTop = c.scrollHeight;
}

async function tryAutoLogin() {
	if (!authToken) return false;
	try {
		const res = await apiRequest('/auth/me', 'GET');
		if (res.status === 200) {
			const d = await res.json();
			document.getElementById('chatUsername').innerText = d.username;
			document.getElementById('authSection').style.display = 'none';
			document.getElementById('chatSection').style.display = 'block';
			return true;
		}
	} catch (e) {}
	localStorage.removeItem('access_token'); authToken = null; return false;
}

async function register() {
	const u = document.getElementById('regUsername').value.trim();
	const p = document.getElementById('regPassword').value;
	if (!u || !p) { showError('regError', 'Username & password required'); return }
	const btn = document.getElementById('registerBtn'); btn.disabled = true;
	try {
		const res = await fetch(API_BASE + '/auth/register', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ username: u, password: p }) });
		const d = await res.json(); if (!res.ok) throw new Error(d.detail || 'Registration failed');
		localStorage.setItem('access_token', d.access_token); authToken = d.access_token; window.location.reload();
	} catch (err) { showError('regError', err.message) } finally { btn.disabled = false }
}

async function login() {
	const u = document.getElementById('loginUsername').value.trim();
	const p = document.getElementById('loginPassword').value; if (!u || !p) { showError('loginError', 'Enter credentials'); return }
	const btn = document.getElementById('loginBtn'); btn.disabled = true;
	try {
		const res = await fetch(API_BASE + '/auth/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ username: u, password: p }) });
		const d = await res.json(); if (!res.ok) throw new Error(d.detail || 'Invalid login');
		localStorage.setItem('access_token', d.access_token); authToken = d.access_token; window.location.reload();
	} catch (err) { showError('loginError', err.message) } finally { btn.disabled = false }
}

async function sendMessage() {
	const input = document.getElementById('messageInput'); const msg = input.value.trim(); if (!msg) return; input.value = '';
	addMessage(msg, true);
	const btn = document.getElementById('sendBtn'); btn.disabled = true; btn.innerText = '...';
	try {
		const res = await apiRequest('/chat', 'POST', { message: msg });
		if (!res.ok) throw new Error((await res.json()).detail || 'Chat failed');
		const d = await res.json(); addMessage(d.reply, false);
	} catch (err) { addMessage('⚠️ ' + err.message, false) } finally { btn.disabled = false; btn.innerText = 'Send'; input.focus() }
}

// --- Syllabus & Notes UI ---
function showSection(name) {
	document.getElementById('chatSection').style.display = name === 'chat' ? 'block' : 'none';
	document.getElementById('syllabusSection').style.display = name === 'syllabus' ? 'block' : 'none';
	document.getElementById('notesSection').style.display = name === 'notes' ? 'block' : 'none';
}

async function loadExams() {
	try {
		const res = await apiRequest('/content/exams', 'GET');
		if (!res.ok) throw new Error('Failed to load exams');
		const exams = await res.json();
		const list = document.getElementById('examsList'); list.innerHTML = '';
		const examSelect = document.getElementById('noteExamSelect'); examSelect.innerHTML = '<option value="">Select exam</option>';
		exams.forEach(e => {
			const btn = document.createElement('button'); btn.innerText = e.name; btn.addEventListener('click', () => showSyllabus(e.id)); list.appendChild(btn);
			const opt = document.createElement('option'); opt.value = e.id; opt.innerText = e.name; examSelect.appendChild(opt);
		});
	} catch (err) { showError('syllabusError', err.message) }
}

async function showSyllabus(examId) {
	try {
		const res = await apiRequest('/content/syllabus/' + examId, 'GET'); if (!res.ok) throw new Error('Failed to load syllabus');
		const s = await res.json();
		const out = document.getElementById('syllabusDetail'); out.innerHTML = `<h4>${s.exam}</h4>` + s.subjects.map(sub => `
			<div><strong>${sub.name}</strong> (${sub.weightage || 'NA'})<ul>` + sub.topics.map(t => `<li>${t.name} — ${t.weightage || ''} — ${t.difficulty || ''}</li>`).join('') + '</ul></div>').join('');
	} catch (err) { showError('syllabusError', err.message) }
}

async function loadSubjectsForExam(examId) {
	if (!examId) return; try {
		const res = await apiRequest('/content/exams/' + examId + '/subjects', 'GET'); if (!res.ok) throw new Error('Failed to load subjects');
		const subs = await res.json(); const subjSel = document.getElementById('noteSubjectSelect'); subjSel.innerHTML = '<option value="">Select subject</option>';
		subs.forEach(s => { const o = document.createElement('option'); o.value = s.id; o.innerText = s.name; subjSel.appendChild(o); });
	} catch (err) { showError('notesError', err.message) }
}

async function loadTopicsForSubject(subjectId) {
	if (!subjectId) return; try {
		const res = await apiRequest('/content/subjects/' + subjectId + '/topics', 'GET'); if (!res.ok) throw new Error('Failed to load topics');
		const topics = await res.json(); const tSel = document.getElementById('noteTopicSelect'); tSel.innerHTML = '<option value="">Select topic</option>';
		topics.forEach(t => { const o = document.createElement('option'); o.value = t.id; o.innerText = t.name; tSel.appendChild(o); });
	} catch (err) { showError('notesError', err.message) }
}

async function saveNote() {
	const title = document.getElementById('noteTitle').value.trim();
	const content = document.getElementById('noteContent').value.trim();
	const topicId = document.getElementById('noteTopicSelect').value || null;
	const isPublic = document.getElementById('notePublic').checked;
	if (!title || !content) { showError('notesError', 'Title and content required'); return }
	try {
		const payload = { title, content, topic_id: topicId ? Number(topicId) : null, is_public: isPublic };
		const res = await apiRequest('/notes', 'POST', payload);
		if (!res.ok) throw new Error((await res.json()).detail || 'Save failed');
		await loadUserNotes();
		showError('notesError', 'Saved');
	} catch (err) { showError('notesError', err.message) }
}

async function loadUserNotes() {
	try {
		const res = await apiRequest('/notes', 'GET'); if (!res.ok) throw new Error('Failed to load notes');
		const notes = await res.json(); const list = document.getElementById('userNotesList'); list.innerHTML = '';
		notes.forEach(n => { const d = document.createElement('div'); d.innerHTML = `<strong>${n.title}</strong> <small>${n.is_public? 'public':''}</small><div>${n.content}</div>`; list.appendChild(d); });
	} catch (err) { showError('notesError', err.message) }
}

document.addEventListener('DOMContentLoaded', async () => {
	document.getElementById('showRegisterLink')?.addEventListener('click', e => { e.preventDefault(); showAuth(false) });
	document.getElementById('showLoginLink')?.addEventListener('click', e => { e.preventDefault(); showAuth(true) });
	document.getElementById('loginBtn')?.addEventListener('click', login);
	document.getElementById('registerBtn')?.addEventListener('click', register);
	document.getElementById('sendBtn')?.addEventListener('click', sendMessage);
	document.getElementById('logoutBtn')?.addEventListener('click', logout);
	document.getElementById('messageInput')?.addEventListener('keydown', e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage() } });

	// Syllabus & Notes event wiring
	document.getElementById('showSyllabusBtn')?.addEventListener('click', async () => { showSection('syllabus'); await loadExams(); });
	document.getElementById('backToChatFromSyllabus')?.addEventListener('click', () => showSection('chat'));
	document.getElementById('showNotesBtn')?.addEventListener('click', async () => { showSection('notes'); await loadExams(); await loadUserNotes(); });
	document.getElementById('backToChatFromNotes')?.addEventListener('click', () => showSection('chat'));
	document.getElementById('noteExamSelect')?.addEventListener('change', e => loadSubjectsForExam(e.target.value));
	document.getElementById('noteSubjectSelect')?.addEventListener('change', e => loadTopicsForSubject(e.target.value));
	document.getElementById('saveNoteBtn')?.addEventListener('click', saveNote);

	const logged = await tryAutoLogin();
	if (!logged) { document.getElementById('authSection').style.display = 'block'; document.getElementById('chatSection').style.display = 'none' }
	else { document.getElementById('authSection').style.display = 'none'; document.getElementById('chatSection').style.display = 'block' }
});
