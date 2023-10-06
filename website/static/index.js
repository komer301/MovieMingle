function addWatchlist(ShowId) {
  fetch("/add-watchlist", {
    method: "POST",
    body: JSON.stringify({ ShowId: ShowId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}
