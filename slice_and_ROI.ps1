#!/usr/bin/env pwsh

$input_dir = $args[0]
$output_dir = $args[1]
$other = $args[2]



If ( $null -eq $input_dir)
{
  Write-Error -Message "Input directory not set" -Category NotSpecified
  exit 1
}
ElseIf (-not (Test-Path -Path $input_dir -PathType Container))
{
  Write-Error -Message "Input directory not found" -Category ObjectNotFound
   exit 1
}


If ($null -eq $output_dir)
{
  Write-Error -Message "Output directory not set" -Category NotSpecified
  exit 1
}
ElseIf ( -not (Test-Path -Path $output_dir -PathType Container) )
{
  Write-Error -Message "Output directory not found" -Category ObjectNotFound
  exit 1
}

$files = Get-ChildItem -Path $input_dir* -Include *.pkl.npy
Write-Output "Found "$files.Length" files to process"


For ($i = 0; $i -lt $files.Length; $i++)
{
  Write-Output  "* Processing " $files[$i]
  $BaseName = Get-Item $files[$i] | Select-Object -ExpandProperty BaseName
  $BaseName = $BaseName -replace "\..+"
  $lung_name = $output_dir + $BaseName

  python -m pipeline.slice_and_ROI --input $files[$i] --output $lung_name $other
  If ( $? )
  {
    Write-Output   "[done]"
  }
  Else
  {
    Write-Output  "[failed]" 
    exit 1
  }
}
