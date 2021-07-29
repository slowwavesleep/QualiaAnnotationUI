window.addEventListener("DOMContentLoaded", function () {

    document.getElementById("submit-button").addEventListener("click", function () {

        let selection = document.getElementById("select-annotation");
        let selectionValue = selection.options[selection.selectedIndex].value;
        let relationId = document.getElementById("relation-id").innerText;


        let url = `/annotate/submit?id=${encodeURIComponent(relationId)}&a=${encodeURIComponent(selectionValue)}`
        // console.log(url);
        // console.log(selectionValue);
        // console.log(relationId);

        fetchAsync(url)

        // console.log(data)



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
  console.log(json.data)
}



// function setSubmissionStatus(result)