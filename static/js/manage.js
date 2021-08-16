window.addEventListener("DOMContentLoaded", function () {
        document.getElementById("reset-all").addEventListener("click", function () {
            let url = `/data/reset`

            let reaction = confirm("This will reinitialize all data from scratch. Continue?")

            if (reaction){
                fetchAsync(url)
            }


    })

        document.getElementById("reset-annotations").addEventListener("click", function () {
            let url = `/annotations/reset`

            let reaction = confirm("This will reset all annotations. Continue?")

            if (reaction){
                fetchAsync(url)
            }


    })

})

async function fetchAsync (url) {
  const response = await fetch(url);
  const json = await response.json();
  window.alert(json.data.result)
}