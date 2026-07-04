document.getElementById("searchForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const matieres = document.getElementById("matieres").value;
    const jour = document.getElementById("jour").value;
    const heure = document.getElementById("heure").value;
    const filiere = document.getElementById("filiere").value;

    const resultsContainer = document.getElementById("resultsContainer");
    resultsContainer.innerHTML = `<p class="text-center text-muted">Recherche en cours...</p>`;

    try {
        const response = await fetch("/search", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ matieres, jour, heure, filiere }),
        });

        const data = await response.json();

        if (!response.ok) {
            resultsContainer.innerHTML = `<div class="alert alert-danger">${data.error || "Erreur inconnue."}</div>`;
            return;
        }

        renderResults(data.resultats);
    } catch (err) {
        resultsContainer.innerHTML = `<div class="alert alert-danger">Erreur de connexion au serveur.</div>`;
        console.error(err);
    }
});

function renderResults(resultats) {
    const container = document.getElementById("resultsContainer");

    if (resultats.length === 0) {
        container.innerHTML = `<div class="alert alert-warning text-center">Aucun mentor compatible trouvé.</div>`;
        return;
    }

    let html = `<h5 class="mb-3">${resultats.length} mentor(s) trouvé(s)</h5>`;

    resultats.forEach((m) => {
        html += `
        <div class="card mb-3 shadow-sm">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-start">
                    <h5 class="card-title mb-1">${m.nom}</h5>
                    <span class="badge bg-success fs-6">${m.score}%</span>
                </div>
                <p class="mb-1"><strong>Matières en commun :</strong> ${m.matieres_communes.join(", ")}</p>
                <p class="mb-1"><strong>Disponibilités :</strong> ${m.disponibilites}</p>
                <p class="mb-1"><strong>Format :</strong> ${formatLabel(m.format)}</p>
                ${m.filiere ? `<p class="mb-0"><strong>Filière :</strong> ${m.filiere}</p>` : ""}
            </div>
        </div>`;
    });

    container.innerHTML = html;
}

function formatLabel(format) {
    const labels = {
        presentiel: "Présentiel",
        en_ligne: "En ligne",
        les_deux: "Présentiel ou en ligne",
    };
    return labels[format] || format;
}
