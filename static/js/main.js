window.addEventListener("DOMContentLoaded", function () {

    document.getElementById("submit-button").addEventListener("click", function () {

        let selection = document.getElementById("select-annotation");
        let selectionValue = selection.options[selection.selectedIndex].value;
        let relationId = document.getElementById("relation-id").innerText;


        let url = `/annotate/submit?id=${encodeURIComponent(relationId)}&a=${encodeURIComponent(selectionValue)}`
        console.log(url);
        console.log(selectionValue);
        console.log(relationId)

        console.log(fetchAsync(url))
    })
})

async function fetchAsync (url) {
  let response = await fetch(url);
  return await response.json();
}