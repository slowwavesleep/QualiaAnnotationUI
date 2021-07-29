window.addEventListener("DOMContentLoaded", function () {

    document.getElementById("submit-button").addEventListener("click", function () {

        let selection = document.getElementById("select-annotation");
        let selectionValue = selection.options[selection.selectedIndex].value;
        let relationId = document.getElementById("relation-id").innerText;


        let url = `/annotate/submit?id=${encodeURIComponent(relationId)}&a=${encodeURIComponent(selectionValue)}`

        fetchAsync(url)

    })

    document.getElementById("reload").addEventListener("click", function () {
        let isSubmitted = document.getElementById("is-submitted").innerText === "Yes"
        if (!isSubmitted) {
            let reaction = confirm("You haven't submitted a label for this relation. Continue anyway?")
            if (reaction) {
                window.location.reload(true)
            }
        } else {
            window.location.reload(true)
        }

    })
})

async function fetchAsync (url) {
  const response = await fetch(url);
  const json = await response.json();
  let isSubmitted = document.getElementById("is-submitted")
  if (json.data.status === "ok") {
      isSubmitted.innerText = "Yes"
  }
  window.alert(json.data.result)
}



// function setSubmissionStatus(result)