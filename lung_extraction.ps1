#!/usr/bin/env pwsh

$input_dir = $args[0]
$output_dir = $args[1]
$optional_1= $args[2]
$optional_2 = $args[3]

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






$files = Get-ChildItem -Path $input_dir* -Include *.pkl.npy
Write-Host "Found "$files.Length" files to process"



#New-Item -Path $output_dir -ItemType directory -Force

For ($i = 0; $i -lt $files.Length; $i++)
{
  Write-Host  "* Processing " $files[$i]
  $BaseName = Get-Item $files[$i] | Select-Object -ExpandProperty BaseName
  $lung_name = $output_dir + $BaseName

  python -m pipeline.lung_extraction --input $files[$i] --lung $lung_name $optional_1 $optional_2
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
