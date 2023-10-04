search = document.getElementById('Search')
table11 = document.getElementById('table1')
table2 = document.getElementById('table2')
tableRows = document.getElementById('result-rows')
error = document.getElementById('no-result')
table2.style.display ="NONE"
search.addEventListener('keyup',(e)=>{
    searchVal =e.target.value;
    if(searchVal.length>0){
        table11.style.display ="NONE"
        table2.style.display ="BLOCK"
        tableRows.innerHTML=''
        fetch("/incomes/search_incomes/",{
            body : JSON.stringify({search:searchVal}) ,
            method : 'post'
        })
        .then(res => res.json())
        .then(data =>{
            if (data.length > 0) {
                error.innerHTML = ''
                data.forEach(income => {
                    tableRows.innerHTML += ( `
                    <tr>
                    <td>${income.amount}</td>
                    <td>${income.description}</td>
                    <td>${income.category}</td>
                    <td>${new Date(income.date).toDateString()}</td>
                    <td>
                       <span><a href="edit-income/${income.id}"><i class="fas fa-edit" style="color: darkgreen;" >  </i></a></span>
                    </td>
                    <td>
                        <span> <a href=""delete-income/${income.id}""><i class="fas fa-trash" style="color: red;"> </i></a></span>
                    </td>
                    </tr>
                        `)
                });
              } else {
                error.innerHTML = `<p class="text-info lead">No Results Found</p>`;
                table2.style.display ="NONE"
              }
        })
        
    }
    else{
        table2.style.display ="NONE"
        table11.style.display ="block"
    }
    

});