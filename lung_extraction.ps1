#!/usr/bin/env pwsh

[CmdletBinding()]
Param
(
  [parameter(mandatory=$true, position=0)][string]$input_dir,
  [parameter(mandatory=$true, position=1)][string]$output_dir
)

If ( $null -eq $input_dir )
{
  Write-Error -Message "Error! Input directory not set" -Category NotSpecified -RecommendedAction "Set path to input directory"
  exit 1
}
ElseIf (-not (Test-Path -Path $input_dir -PathType Container))
{
  Write-Error -Message "Error! Input directory not found" -Category NotSpecified
}


If ( $null -eq $output_dir)
{
  Write-Error -Message "Error! Output directory not set" -Category NotSpecified-RecommendedAction "Set path to output directory"
  exit 1
}
ElseIf ( -not (Test-Path -Path $output_dir -PathType Container) )
{
  Write-Error -Message "Error! Output directory not found" -Category NotSpecified
  exit 1
}






$files = get-ChildItem -Path $input_dir*
Write-Output "Found "$files.Length" files to process"


For ($i = 0; $i -lt $files.Length; $i++)
{
  Write-Output  "* Processing " $files[$i]
  $BaseName = Get-Item $files[$i] | Select-Object -ExpandProperty BaseName
  $BaseName = $BaseName -replace "\..+"
  $lung_name = $output_dir + $BaseName + +".nrrd"

  python -m CTLungSeg.lung_extraction --input $files[$i] --output $lung_name
  If ( $? )
  {
    Write-Output  -InputObject "[done]"
  }
  Else
  {
    Write-Output -InputObject "[failed]"
    exit 1
  }
}
