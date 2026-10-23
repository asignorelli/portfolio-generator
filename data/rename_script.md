RUN THIS IN TERMINAL TO RENAME RESUMES TO NUMBERS:

cd data\resumes
$mapFile = "..\id_mapping.csv"

# highest existing ID (files already named 0001, 0002, ...)
$existing = Get-ChildItem -File | Where-Object { $_.BaseName -match '^\d{4}$' }
$i = if ($existing) { ($existing | ForEach-Object { [int]$_.BaseName } | Measure-Object -Maximum).Maximum + 1 } else { 1 }

# only the new, not-yet-renamed files
$new = Get-ChildItem -File | Where-Object { $_.BaseName -notmatch '^\d{4}$' } | Sort-Object Name

$rows = foreach ($f in $new) {
    $id = "{0:D4}" -f $i
    [pscustomobject]@{ sample_id = $id; original_name = $f.Name }
    Rename-Item -LiteralPath $f.FullName -NewName ($id + $f.Extension)
    $i++
}

if ($rows) { $rows | Export-Csv $mapFile -NoTypeInformation -Append }