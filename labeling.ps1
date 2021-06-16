#!/usr/bin/env pwsh

[CmdletBinding()]
Param
(
  [parameter(mandatory=$true, position=0)][string]$input_dir,
  [parameter(mandatory=$true, position=1)][string]$label_dir,
  [parameter(mandatory=$false, position=2)][string]$centroids=""
)



If ( $null -eq $input_dir )
{
  Write-Error -Message "Error! Input directory not set" -Category NotSpecified
  exit 1
}
ElseIf (-not (Test-Path -Path $input_dir -PathType Container))
{
  Write-Error -Message "Error! Input directory not found" -Category ObjectNotFound
  exit 1
}


If ( $null -eq $centroids)
{
  $centroids = ""
}
ElseIf ( -not (Test-Path $centroids) )
{
  Write-Error -Message "Error! Centroids file not found" -Category ObjectNotFound
  exit 1
}


If ( $null -eq $label_dir)
{
  Write-Error -Message "Error! Output directory for label 1 not set"-Category NotSpecified
  exit 1
}
ElseIf ( -not (Test-Path -Path $label_dir -PathType Container) )
{
  Write-Error -Message "Error! Output directory for label1 not found" -Category ObjectNotFound
  exit 1
}






$files = get-ChildItem -Path $input_dir*
Write-Output "Found "$files.Length" files to process"


For ($i = 0; $i -lt $files.Length; $i++)
{
  Write-Output  "* Processing " $files[$i]
  $BaseName = Get-Item $files[$i] | Select-Object -ExpandProperty BaseName
  $BaseName = $BaseName -replace "\..+"
  $label_name = $label_dir + $BaseName +".nrrd"



  python -m CTLungSeg.labeling --input $files[$i] --centroids $centroids --output $label_name

  If ( $? )
  {
    Write-Output  '[done]'
  }
  Else
  {
    Write-Output '[failed]'
    exit 1
  }
}
