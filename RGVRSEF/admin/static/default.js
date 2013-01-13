function deleteConfirm(var1,var2,var3)
{
    var3 = var3||'delete'
    return confirm("Are you sure you want to "+var3+": "+var1+", "+var2+"?")
}

function resendComfirm(var1)
{
    return confirm("Are you sure you want to resend all "+var1+" confirmations?")
}

function toggle(showHideDiv,switchTextDiv)
{
    var ele = document.getElementById(showHideDiv);
    var text = document.getElementById(switchTextDiv);
    var inner = text.innerHTML

    if (ele.style.display == "block")
    {
        ele.style.display = "none";
        text.innerHTML = inner.replace("Hide","Show");
    }
    else
    {
        ele.style.display = "block";
        text.innerHTML = inner.replace("Show","Hide");
    }
}

function toggleHover(showHideDiv)
{
    var ele = document.getElementById(showHideDiv);

    if (ele.style.display == "block")
    {
        ele.style.display = "none";
    }
    else
    {
        ele.style.display = "block";
    }
}
        

