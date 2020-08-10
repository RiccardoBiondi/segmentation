
$input_dir = $args[0]
$output_dir = $args[1]
$centroids = $args[2]



If ( $input_dir -eq $null )
{
  Write-Host "Error! Input directory not set" -ForegroundColor Red
  exit 1
}
ElseIf (-not (Test-Path -Path $input_dir -PathType Container))
{
  Write-Host "Error! Input directory not found" -ForegroundColor Red
  exit 1
}


If ( $output_dir -eq $null )
{
  Write-Host "Error! Output directory not set" -ForegroundColor Red
  exit 1
}
ElseIf ( -not (Test-Path -Path $output_dir -PathType Container) )
{
  Write-Host "Error! Output directory not found" -ForegroundColor Red
  exit 1
}


If ( $centroids -eq $null )
{
  Write-Host "Error! No centroids provided" -ForegroundColor Red
  exit 1
}
ElseIf ( -not (Test-Path -Path $centroids -PathType Container) )
{
  Write-Host "Error! Centroids file not found" -ForegroundColor Red
  exit 1
}


$files = Get-ChildItem -Path $input_dir* -Include *.pkl.npy
Write-Host "Found "$files.Length" files to process"


For ($i = 0; $i -lt $files.Length; $i++)
{
  Write-Host  "* Processing " $files[$i]
  $BaseName = Get-Item $files[$i] | Select-Object -ExpandProperty BaseName
  $lung_name = $output_dir + $BaseName

  python -m pipeline.labeling --input $files[$i] --output $lung_name --centroids $centroids
  If ( $? )
  {
    Write-Host -NoNewLine "[done]" -ForegroundColor Green
  }
  Else
  {
    Write-Host -NoNewLine "[failed]" -ForegroundColor Red
    exit 1
  }
}
